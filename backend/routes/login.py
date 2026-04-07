import jwt
from bson import ObjectId

from database import mongo_users, mongo_passwd_resets
from datetime import datetime, timedelta
from fastapi import APIRouter, Body, HTTPException, Depends
from pydantic import BaseModel, Field
import bcrypt
import config.config as config
import auth
from schemas.global_schema import DefReq
from typing import Optional

import random
import string


router = APIRouter()

class LoginReq(BaseModel):
    username: str = Field(..., title="Login", description="Login użytkownika")
    password: str = Field(..., title="Hasło", description="Hasło użytkownika")

class LoginResp(BaseModel):
    token: str = Field(..., title="Token", description="Token użytkownika")


@router.post("", response_model=LoginResp, responses={401: {"description": "Niepoprawne dane logowania"}}, name="Logowanie, zwraca token użytkownika")
async def login(login_req: LoginReq = Body(...)):
    user = await mongo_users.find_one({"username": login_req.username}, {"_id": 1, "password": 1})
    if not user:
        raise HTTPException(status_code=401, detail="Niepoprawne dane logowania")

    if not bcrypt.checkpw(login_req.password.encode(), user["password"].encode()):
        raise HTTPException(status_code=401, detail="Niepoprawne dane logowania")
    
    
    user["_id"] = str(ObjectId(user["_id"]))


    token = jwt.encode({
        "id_user": user["_id"],
        "username": login_req.username
    }, config.JWT_SECRET, algorithm="HS256")

    return LoginResp(token=token)


class VerifyOK(BaseModel):
    status: str = Field(..., title="Status", description="Status weryfikacji, ok lub zwraca 401")

# 401
@router.post("/verify", response_model=VerifyOK, responses={401: {"description": "Niepoprawny token"}}, name="Raczej nieużywany")
async def verify(token: DefReq):
    authAns = auth.verifyUser(token)

    if not authAns:
        raise HTTPException(status_code=401, detail="Niepoprawny token")
    return {"status": "ok"}




class ResetPasswordReq(BaseModel):
    username: Optional[str] = Field(None, title="Login", description="Login użytkownika LUB")
    email: Optional[str] = Field(None, title="Email", description="Email użytkownika LUB")

class ResetPasswordResp(BaseModel):
    status: str = Field(..., title="Status", description="Status resetu hasła, ok lub zwraca 404 jeśli nie znaleziono użytkownika")

@router.post("/resetPassword", response_model=ResetPasswordResp, responses={404: {"description": "Nie znaleziono użytkownika"}}, description="Wysyła maila z linkiem do resetu hasła", name="Żądanie resetu hasła")
async def reset_password(reset_password_req: ResetPasswordReq = Body(...)):
    if reset_password_req.username:
        user = await mongo_users.find_one({"username": reset_password_req.username}, {"email": 1})
    elif reset_password_req.email:
        user = await mongo_users.find_one({"email": reset_password_req.email}, {"email": 1})
    else:
        raise HTTPException(status_code=404, detail="Nie znaleziono użytkownika")

    if not user:
        raise HTTPException(status_code=404, detail="Nie znaleziono użytkownika")

    # send email with reset link
    # add reset token to db

    reset_token = ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(32))
    await mongo_passwd_resets.insert_one({
        "id_user": str(ObjectId(user["_id"])),
        "reset_token": reset_token,
        "expire_at": datetime.utcnow() + timedelta(hours=1)
    })

    # TODO send email

    return ResetPasswordResp(status="ok")


class ChangePasswordReq(BaseModel):
    reset_token: str = Field(..., title="Token resetu", description="Token resetu hasła (z maila)")
    new_password: str = Field(..., title="Nowe hasło", description="Nowe hasło użytkownika")

class ChangePasswordResp(BaseModel):
    status: str = Field(..., title="Status", description="Status zmiany hasła, ok lub zwraca 401")

@router.post("/changePassword", response_model=ChangePasswordResp, responses={401: {"description": "Niepoprawny token resetu hasła bądź wygasł"}}, description="Zmienia hasło użytkownika", name="Zmiana hasła")
async def change_password(change_password_req: ChangePasswordReq = Body(...)):
    # check if reset_token exists and is not expired
    # change password
    # remove reset_token from db and all other tokens which are expired

    reset = await mongo_passwd_resets.find_one({"reset_token": change_password_req.reset_token})
    if not reset:
        raise HTTPException(status_code=401, detail="Niepoprawny token resetu hasła (z maila)")
    
    if reset["expire_at"] < datetime.utcnow():
        raise HTTPException(status_code=401, detail="Token resetu hasła wygasł")
    
    salt = bcrypt.gensalt()
    password = bcrypt.hashpw(change_password_req.new_password.encode(), salt)

    await mongo_users.update_one({"_id": ObjectId(reset["id_user"])}, {"$set": {"password": password.decode()}})
    await mongo_passwd_resets.delete_many({"id_user": reset["id_user"]})
    await mongo_passwd_resets.delete_many({"expire_at": {"$lt": datetime.utcnow()}})

    return ChangePasswordResp(status="ok")