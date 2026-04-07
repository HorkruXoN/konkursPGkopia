from fastapi import Body, APIRouter, HTTPException
from schemas.global_schema import DefReq
from bson.objectid import ObjectId
from database import mongo_users, mongo_chats, mongo_messages
from pydantic import BaseModel, Field
from typing import Optional
from auth import verifyUser

router = APIRouter()
class MeResp(BaseModel):
    id_user: str = Field(..., title="ID", description="ID użytkownika")
    username: str = Field(..., title="Login", description="Login użytkownika")
    full_name: str = Field(..., title="Pełna nazwa", description="Pełna nazwa użytkownika")
    chats: list = Field(..., title="Rozmowy", description="Lista czatów użytkownika")

    # example
    class Config:
        json_schema_extra = {
            "example": {
                "id_user": "65c8d2f51ca9a8cdc06a58c2",
                "username": "johndoe",
                "full_name": "John Doe",
                "chats": [
                    {
                    "id_chat": "65c91c8f1ca9a8cdc06a58d9",
                    "last_message": {
                        "content": "tak dokladnie",
                        "date": "2024-02-11T11:00:00Z",
                        "id_user": "65c8d2f51ca9a8cdc06a58c2"
                    },
                    "name": "Alice Johnson",
                    "is_group": False,
                    "members": [
                        "65c8d2f51ca9a8cdc06a58c4"
                    ],
                    "unread_messages": 0
                    },
                    {
                    "id_chat": "65c91c8f1ca9a8cdc06a58d3",
                    "last_message": {
                        "content": "nie krzycz prosze",
                        "date": "2024-02-11T10:00:00Z",
                        "id_user": "65c8d2f51ca9a8cdc06a58c3"
                    },
                    "name": "Jane Smith",
                    "is_group": False,
                    "members": [
                        "65c8d2f51ca9a8cdc06a58c3"
                    ],
                    "unread_messages": 0
                    },
                    {
                    "id_chat": "65c91c8f1ca9a8cdc06a58d4",
                    "last_message": {
                        "content": "420",
                        "date": "2024-02-11T10:00:00Z",
                        "id_user": "65c8d2f51ca9a8cdc06a58c9"
                    },
                    "name": "grupa2",
                    "is_group": True,
                    "members": [
                        "65c8d2f51ca9a8cdc06a58c6",
                        "65c8d2f51ca9a8cdc06a58c9",
                        "65c8d2f51ca9a8cdc06a58c3",
                        "65c8d2f51ca9a8cdc06a58c4"
                    ],
                    "unread_messages": 0
                    },
                    {
                    "id_chat": "65c91c8f1ca9a8cdc06a58d5",
                    "last_message": {
                        "content": "jestem w polowie essa",
                        "date": "2024-02-11T10:00:00Z",
                        "id_user": "65c8d2f51ca9a8cdc06a58c6"
                    },
                    "name": "Emily Davis",
                    "is_group": False,
                    "members": [
                        "65c8d2f51ca9a8cdc06a58c6"
                    ],
                    "unread_messages": 0
                    },
                    {
                    "id_chat": "65c91c8f1ca9a8cdc06a58d6",
                    "last_message": {
                        "content": "pudzian transpor",
                        "date": "2024-02-11T10:00:00Z",
                        "id_user": "65c8d2f51ca9a8cdc06a58c2"
                    },
                    "name": "grupa3",
                    "is_group": True,
                    "members": [
                        "65c8d2f51ca9a8cdc06a58c5",
                        "65c8d2f51ca9a8cdc06a58c7",
                        "65c8d2f51ca9a8cdc06a58c8"
                    ],
                    "unread_messages": 0
                    },
                    {
                    "id_chat": "65c91c8f1ca9a8cdc06a58d7",
                    "last_message": {
                        "content": "lotus bloume cos tam genau",
                        "date": "2024-02-11T10:00:00Z",
                        "id_user": "65c8d2f51ca9a8cdc06a58c2"
                    },
                    "name": "Sophia Martinez",
                    "is_group": False,
                    "members": [
                        "65c8d2f51ca9a8cdc06a58c8"
                    ],
                    "unread_messages": 0
                    },
                    {
                    "id_chat": "65c91c8f1ca9a8cdc06a58d8",
                    "last_message": {
                        "content": "mineralwasser",
                        "date": "2024-02-11T10:00:00Z",
                        "id_user": "65c8d2f51ca9a8cdc06a58c2"
                    },
                    "name": "grupa4",
                    "is_group": True,
                    "members": [
                        "65c8d2f51ca9a8cdc06a58c5",
                        "65c8d2f51ca9a8cdc06a58c9",
                        "65c8d2f51ca9a8cdc06a58c6"
                    ],
                    "unread_messages": 0
                    }
                ]
            }
        }

@router.post("", response_model=MeResp, responses={401: {"description": "Niepoprawny token"}})
async def me(me_req: DefReq = Body(...)):
    user = verifyUser(me_req.token)
    
    if not user:
        raise HTTPException(status_code=401, detail="Niepoprawny token")

    user_id = user["id_user"]

    res = {"id_user": user_id}

    user = await mongo_users.find_one({"_id": ObjectId(user_id)})
    res["username"] = user["username"]
    res["full_name"] = user["full_name"]

    chats_list = []
    userChats = await mongo_chats.find({"members.user_id": user_id}).to_list(length=1000)

    for chat in userChats:
        chat_id = str(ObjectId(chat["_id"]))
        last_message = await mongo_messages.find_one({"id_chat": chat_id}, sort=[("date", -1)])
        last_message = {
            "content": last_message["content"],
            "date": last_message["date"],
            "id_user": last_message["id_user"]
        }
        
        members = chat["members"]
        members = [member["user_id"] for member in members if member["user_id"] != user_id]

        unread_messages = [member["unread_messages"] for member in chat["members"] if member["user_id"] == user_id][0]

        if chat["is_group"]:
            name = chat["name"]
        else:
            member = await mongo_users.find_one({"_id": ObjectId(members[0])})
            name = member["full_name"]
        chat = {
            "id_chat": chat_id,
            "last_message": last_message,
            "name": name,
            "is_group": chat["is_group"],
            "members": members,
            "unread_messages": unread_messages
        }
        chats_list.append(chat)
    
    chats_list.sort(key=lambda x: x["last_message"]["date"], reverse=True)
    res["chats"] = chats_list


    return res
        