from fastapi import Body, APIRouter, HTTPException, File, Response, UploadFile
from pydantic import BaseModel, Field
from typing import Optional
from database import mongo_users
import bcrypt
import random
import string
from bson import ObjectId

import os

from auth import create_user, verifyUser

router = APIRouter()


# STWORZENIE UŻYTKOWNIKA

class CreateUserReq(BaseModel):
    token: str = Field(..., title="Token", description="Token użytkownika z uprawnieniami administratora")
    username: str = Field(..., title="Login", description="Login nowego użytkownika")
    email: str = Field(..., title="Email", description="Email nowego użytkownika")
    name: str = Field(..., title="Imię", description="Imię nowego użytkownika")
    surname: str = Field(..., title="Nazwisko", description="Nazwisko nowego użytkownika")

class CreateUserResp(BaseModel):
    id_user: str = Field(..., title="ID", description="ID stworzonego użytkownika")

@router.post("/createUser", response_model=CreateUserResp, responses={401: {"description": "Niepoprawny token lub brak uprawnień"}})
async def create_user_f(req: CreateUserReq):
    user = {
        "username": req.username,
        "email": req.email,
        "full_name": req.name + " " + req.surname,
    }
    
    # dodać sprawdzanie czy admin
    user = verifyUser(req.token)

    if not user:
        raise HTTPException(status_code=401, detail="Niepoprawny token lub brak uprawnień")
    
    is_admin = await mongo_users.find_one({"_id": ObjectId(user["id_user"])})
    
    if not is_admin["is_admin"]:
        raise HTTPException(status_code=401, detail="Niepoprawny token lub brak uprawnień")

    
    id_user = await create_user(username=req.username, email=req.email, full_name=req.name + " " + req.surname)
    if not id_user:
        raise HTTPException(status_code=400, detail="Użytkownik o podanym loginie już istnieje")


    response = CreateUserResp(id_user=str(id_user))
    return response

class RemoveUserReq(BaseModel):
    token: str = Field(..., title="Token", description="Token użytkownika z uprawnieniami administratora")
    id_user: str = Field(..., title="ID", description="ID użytkownika do usunięcia")

class RemoveUserResp(BaseModel):
    status: str = Field(..., title="Status", description="Status usunięcia, ok lub zwraca 400 lub 401")

@router.post("/removeUser", response_model=RemoveUserResp, responses={401: {"description": "Niepoprawny token lub brak uprawnień"}, 400: {"description": "Użytkownik o podanym ID nie istnieje"}})
async def remove_user(req: RemoveUserReq):
    admin_user = verifyUser(req.token)

    # dodać sprawdzanie czy admin
    if not admin_user:
        raise HTTPException(status_code=401, detail="Niepoprawny token lub brak uprawnień")
    


    user = await mongo_users.find_one({"_id": ObjectId(req.id_user)})
    if not user:
        raise HTTPException(status_code=400, detail="Użytkownik o podanym ID nie istnieje")

    await mongo_users.delete_one({"_id": ObjectId(req.id_user)})

    return RemoveUserResp(status="ok")