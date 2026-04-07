from fastapi import Body, APIRouter, HTTPException, Response
from pydantic import BaseModel, Field
from typing import Optional
import os

from schemas.global_schema import DefReq

from database import mongo_users
from bson import ObjectId

from database import mongo_users
from auth import verifyUser
import re

router = APIRouter()

class UserResp(BaseModel):
    full_name: str = Field(..., title="Pełna nazwa", description="Pełna nazwa użytkownika")
    image_url: str = Field(..., title="URL obrazka", description="URL obrazka użytkownika")
    
    # example
    class Config:
        json_schema_extra = {
            "example": {   
                "full_name": "Mariusz Pudzianowski",
                "image_url": "http://localhost:8000/img/5f8e5f9e7e4f8d0b5b4c8d4e"
            }
        }

class UsersResp(BaseModel):
    users: list = Field(..., title="Użytkownicy", description="Lista użytkowników z ich danymi")
    
    # example
    class Config:
        json_schema_extra = {
            "example": {
                "users": [
                    {
                    "full_name": "Jane Smith",
                    "is_active": True,
                    "last_seen": "2024-02-11T10:00:00Z",
                    "id_user": "65c8d2f51ca9a8cdc06a58c3"
                    },
                    {
                    "full_name": "Alice Johnson",
                    "is_active": False,
                    "last_seen": "2024-02-10T15:45:00Z",
                    "id_user": "65c8d2f51ca9a8cdc06a58c4"
                    },
                    {
                    "full_name": "Bob Brown",
                    "is_active": True,
                    "last_seen": "2024-02-11T11:20:00Z",
                    "id_user": "65c8d2f51ca9a8cdc06a58c5"
                    },
                    {
                    "full_name": "Emily Davis",
                    "is_active": True,
                    "last_seen": "2024-02-11T08:15:00Z",
                    "id_user": "65c8d2f51ca9a8cdc06a58c6"
                    },
                    {
                    "full_name": "Michael Wilson",
                    "is_active": True,
                    "last_seen": "2024-02-10T19:10:00Z",
                    "id_user": "65c8d2f51ca9a8cdc06a58c7"
                    },
                    {
                    "full_name": "Sophia Martinez",
                    "is_active": False,
                    "last_seen": "2024-02-10T22:30:00Z",
                    "id_user": "65c8d2f51ca9a8cdc06a58c8"
                    },
                    {
                    "full_name": "David Anderson",
                    "is_active": True,
                    "last_seen": "2024-02-11T07:45:00Z",
                    "id_user": "65c8d2f51ca9a8cdc06a58c9"
                    },
                    {
                    "full_name": "Administrator",
                    "is_active": False,
                    "last_seen": "1900-01-01 00:00:00",
                    "id_user": "65c979c52d15ed29725b1b4e"
                    },
                    {
                    "full_name": "WIN-RUI2QN5P9MS",
                    "is_active": False,
                    "last_seen": "1900-01-01 00:00:00",
                    "id_user": "65c979c52d15ed29725b1b4f"
                    },
                    {
                    "full_name": "Andrzej",
                    "is_active": False,
                    "last_seen": "1900-01-01 00:00:00",
                    "id_user": "65c979c52d15ed29725b1b50"
                    },
                    {
                    "full_name": "Andrzej Duda",
                    "is_active": False,
                    "last_seen": "1900-01-01 00:00:00",
                    "id_user": "65c979c52d15ed29725b1b51"
                    }
                ]
            }
        }



@router.post("", response_model=UsersResp, responses={401: {"description": "Niepoprawny token"}})
async def users(users_req: DefReq = Body(...)):
    user = verifyUser(users_req.token)
    if not user:
        raise HTTPException(status_code=401, detail="Niepoprawny token")
    

    # get _id, full_name, is_active, last_seen from users

    users_list = await mongo_users.find({}, {"_id": 1, "full_name": 1, "is_active": 1, "last_seen": 1}).to_list(length=1000)

    for ul in users_list:
        ul["id_user"] = str(ObjectId(ul["_id"]))
        ul.pop("_id")

    # remove id_user from list
    for ul in users_list:
        if ul["id_user"] == user["id_user"]:
            users_list.remove(ul)
            break
        

    return {"users": users_list}


@router.get("/image", responses={200: {"description": "Zwraca obrazek użytkownika lub domyślny jeśli nie znajdzie"}})
async def get_image(id_user: str):
    if not re.match(r"^[0-9a-f]{24}$", id_user):
        return Response(content=open("img/default.png", "rb").read(), media_type="image/png")

    filename = f"{id_user}.png"

    
    if not os.path.isfile(f"img/{filename}"):
        return Response(content=open("img/default.png", "rb").read(), media_type="image/png")
    
    return Response(content=open(f"img/{filename}", "rb").read(), media_type="image/png")



@router.post("/changePhoto")
async def change_photo():
    pass