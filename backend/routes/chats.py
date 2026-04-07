from fastapi import Body, APIRouter, HTTPException, File, Response, UploadFile
from fastapi.responses import FileResponse
from pydantic import BaseModel, Field
from typing import Optional

import os
from database import mongo_chats, mongo_messages, mongo_users
from bson.objectid import ObjectId
from schemas.global_schema import DefReq

from auth import verifyUser

from datetime import datetime

import random
import string


router = APIRouter()


# TWORZENIE NOWEGO CHATU GRUPOWEGO

class CreateChatReq(BaseModel):
    token: str = Field(..., title="Token", description="Token użytkownika")
    type: str = Field(..., title="Typ", description="group/user - group jeśli więcej niż 2 osoby")
    #name if type == group
    name: Optional[str] = Field(None, title="Nazwa", description="Nazwa grupy")
    members: list = Field(..., title="Członkowie", description="Lista członków chatu bez twórcy")

class CreateChatResp(BaseModel):
    id_chat: str = Field(..., title="ID", description="ID stworzonego chatu (JEŚLI ISTNIEJE JUŻ TAKI CHAT TO ZWRACA ID ISTNIEJĄCEGO)")
    is_group: bool = Field(..., title="Typ", description="Typ chatu")
    members: list = Field(..., title="Członkowie", description="Lista członków chatu")
    name: Optional[str] = Field(None, title="Nazwa", description="Nazwa grupy")
    admin: Optional[str] = Field(None, title="Admin", description="ID admina grupy")

@router.post("/createChat", response_model=CreateChatResp, responses={401: {"description": "Niepoprawny token"}})
async def create_chat(req: CreateChatReq):
    user = verifyUser(req.token)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid token")
    
    id_user = user["id_user"]

    members = req.members
    members.append(id_user)

    # check if chat is group
    is_group = False
    if req.type == "group":
        is_group = True


    if not is_group:
        # check if chat exists
        chat = await mongo_chats.find_one({"members": {"$all": members, "$size": 2}})
        if chat:
            members_without_user = [member for member in members if member != id_user]
            return {
                "id_chat": str(chat["_id"]),
                "is_group": False,
                "members": members_without_user
            }

    # create chat
    chat = {
        "is_group": is_group,
        "members": [{"user_id": member, "unread_messages": 0} for member in members]
    }
    if is_group:
        chat["admin"] = id_user
        chat["name"] = req.name

    res = await mongo_chats.insert_one(chat)
    chat_id = str(res.inserted_id)


    response = {
        "id_chat": chat_id,
        "is_group": is_group,
        "members": chat["members"]
    }
    if is_group:
        response["name"] = chat["name"]
        response["admin"] = chat["admin"]


    await mongo_messages.insert_one({
        "id_chat": chat_id,
        "id_user": id_user,
        "content": "Witaj w nowym czacie!",
        # date like 2024-02-11T10:00:00Z
        "date": datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ")
    })

    return response


# DODAWANIE UŻYTKOWNIKA DO CHATU GRUPOWEGO

class AddUserToChatReq(BaseModel):
    token: str = Field(..., title="Token", description="Token użytkownika")
    id_chat: str = Field(..., title="ID", description="ID chatu")
    members: list = Field(..., title="Członkowie", description="Lista członków chatu do dodania")

class AddUserToChatResp(BaseModel):
    id_chat: str = Field(..., title="ID", description="ID chatu")
    is_group: bool = Field(..., title="Typ", description="Typ chatu")
    members: list = Field(..., title="Członkowie", description="Lista członków chatu")
    name: Optional[str] = Field(None, title="Nazwa", description="Nazwa grupy")
    admin: Optional[str] = Field(None, title="Admin", description="ID admina grupy")



@router.post("/addUser", response_model=AddUserToChatResp, responses={401: {"description": "Niepoprawny token"}, 400: {"description": "Chat is not group chat"}, 403: {"description": "User is not admin of this chat"}, 404: {"description": "Chat not found"}})
async def add_user_to_chat(req: AddUserToChatReq):
    user = verifyUser(req.token)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid token")
    
    id_user = user["id_user"]

    # check if chat is group and user is admin
    chat = await mongo_chats.find_one({"_id": ObjectId(req.id_chat)})
    if not chat:
        raise HTTPException(status_code=404, detail="Chat not found")
    
    if not chat["is_group"]:
        raise HTTPException(status_code=400, detail="Chat is not group chat")
    
    if chat["admin"] != id_user:
        raise HTTPException(status_code=403, detail="User is not admin of this chat")
    
    # add user to chat
    members = chat["members"]

    
    # get req.members full names
    users_names = await mongo_users.find({"_id": {"$in": [ObjectId(member) for member in req.members]}}, {"full_name": 1}).to_list(length=len(req.members))

    for member in req.members:
        if member not in [member["user_id"] for member in members]:
            members.append({"user_id": member, "unread_messages": 0})

    await mongo_chats.update_one({"_id": ObjectId(req.id_chat)}, {"$set": {"members": members}})


    users_names = ", ".join([user["full_name"] for user in users_names])
    # send message to chat
    await mongo_messages.insert_one({
        "id_chat": req.id_chat,
        "id_user": id_user,
        "content": "Użytkownicy {} dołączyli do czatu!".format(users_names),
        # date like 2024-02-11T10:00:00Z
        "date": datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ")
    })

    return {
        "id_chat": req.id_chat,
        "is_group": True,
        "members": members,
        "name": chat["name"],
        "admin": chat["admin"]
    }



class HistoryResp(BaseModel):
    messages: list = Field(..., title="Wiadomości", description="Lista wiadomości z id_user, content, date")


# HISTORIA
@router.post("/{id_chat}/messages", response_model=HistoryResp, responses={401: {"description": "Niepoprawny token"}})
async def messages(id_chat: str, req: DefReq = Body(...)):
    user = verifyUser(req.token)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid token")


    id_user = user["id_user"]
    id_chat = ObjectId(id_chat)

    # get unread messages
    chat = await mongo_chats.find_one({"_id": id_chat})
    members = chat["members"]
    unread_messages = int([member["unread_messages"] for member in members if member["user_id"] == id_user][0])

    
    unread_messages += 50
    messages = await mongo_messages.find({"id_chat": str(id_chat)}).sort([("date", -1)]).to_list(length=unread_messages)

    # mark messages as read
    await mongo_chats.update_one({"_id": ObjectId(id_chat), "members.user_id": id_user}, {"$set": {"members.$.unread_messages": 0}})


    messages_resp = []
    for message in messages:
        messages_resp.append({
            "id_user": str(message["id_user"]),
            "content": message["content"],
            "date": message["date"]
        })

    messages_resp.reverse()
    
    return {"messages": messages_resp}


@router.post("/{id_chat}/messagesAll", response_model=HistoryResp, responses={401: {"description": "Niepoprawny token"}})
async def messages(id_chat: str, req: DefReq = Body(...)):
    user = verifyUser(req.token)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid token")


    id_user = user["id_user"]
    id_chat = ObjectId(id_chat)

    messages = await mongo_messages.find({"id_chat": str(id_chat)}).sort([("date", 1)]).to_list(length=1000)

    messages_resp = []
    for message in messages:
        messages_resp.append({
            "id_user": str(message["id_user"]),
            "content": message["content"],
            "date": message["date"]
        })
    
    return {"messages": messages_resp}
    

# ZDJĘCIE = DO ZROBIENIA PO STRONIE KLIENTA






@router.get("/image")
async def get_image(id_chat: str, id_user_asking: str):
    # get type of chat
    chat = await mongo_chats.find_one({"_id": ObjectId(id_chat)})
    if not chat:
        raise HTTPException(status_code=404, detail="Chat not found")
    
    
    if chat["is_group"]:
        return Response(content=open("img/chat.png", "rb").read(), media_type="image/png")

    member = [member["user_id"] for member in chat["members"] if member["user_id"] != id_user_asking][0]
    filename = f"{member}.png"
    
    if not os.path.isfile(f"img/{filename}"):
        return Response(content=open("img/default.png", "rb").read(), media_type="image/png")
    
    return Response(content=open(f"img/{filename}", "rb").read(), media_type="image/png")




@router.post("/file")
async def save_file(file: UploadFile = File(...), id_chat: str = Body(...), token: str = Body(...)):
    user = verifyUser(token)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid token")

    # save file

    random_chars = ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(10))
    # add random chars to filename before extension
    filename = file.filename.split(".")
    filename[0] += random_chars
    filename = ".".join(filename)

    await mongo_messages.insert_one({
        "id_chat": id_chat,
        "id_user": user["id_user"],
        "content": "chatfile://" + filename,
        "date": datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ")
    })


    with open(f"static/{filename}", "wb") as buffer:
        buffer.write(file.file.read())

@router.get("/file/{filename}")
async def get_file(filename: str):
    if os.path.isfile(f"static/{filename}"):
        return FileResponse(f"static/{filename}")
    raise HTTPException(status_code=404, detail="File not found")


    
    return {"filename": filename}

