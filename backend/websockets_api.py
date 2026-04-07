from fastapi import FastAPI, Request, WebSocket, WebSocketDisconnect, APIRouter
from database import mongo_users, mongo_chats, mongo_messages
from auth import verifyUser
from bson import ObjectId
from datetime import datetime
import json

import string
import random


"""
[
    "<USER_ID>":{
        "socket": <WEBSOCKET>,
    }
]
"""

router = APIRouter()

# WEBSOCKETS
class ConnectionManager:
    def __init__(self):
        self.active_connections: dict = {}

    def get_active_connections(self, id_user: str):
        return self.active_connections.get(id_user, [])

    async def connect(self, websocket: WebSocket, token: str):
        await websocket.accept()

        if self.active_connections.get(token['id_user']) is None:
            self.active_connections[token['id_user']] = []

        self.active_connections[token['id_user']].append(websocket)
        print(self.active_connections)
        # is_active = True
        # last_seen = datetime.now()
        date = datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ")
        mongo_users.update_one({"_id": ObjectId(token['id_user'])}, {"$set": {"is_active": True, "last_seen": date}})

    def disconnect(self, websocket: WebSocket):
        for key, value in self.active_connections.items():
            if websocket in value:
                value.remove(websocket)
                if len(value) == 0:
                    del self.active_connections[key]
                    # is_active = False
                    # last_seen = datetime.now()
                    date = datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ")
                    mongo_users.update_one({"_id": ObjectId(key)}, {"$set": {"is_active": False, "last_seen": date}})

                print(self.active_connections)
                return

    async def send_to(self, user_id: str, message: str):
        if self.active_connections.get(user_id) is not None:
            for connection in self.active_connections[user_id]:
                await connection.send_text(message)

    async def broadcast(self, message: str):
        for connection in self.active_connections:
            await connection.send_text(message)

wsManager = ConnectionManager()

# dodać username i token do parametru
@router.websocket("/connect/{token}")
async def websocket_endpoint(websocket: WebSocket, token: str):
    token = verifyUser(token)
    if not token:
        await websocket.close()
        return

    await wsManager.connect(websocket, token=token)
    try:
        while True:
            data = await websocket.receive_text()
            try:
                data = json.loads(data)
                if data["type"] == "message":
                    # put in database
                    id_chat = data["data"]["id_chat"]
                    message = data["data"]["message"]

                    date = datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ")



                    await mongo_messages.insert_one({
                        "id_chat": id_chat,
                        "id_user": token["id_user"],
                        "content": message,
                        "date": date
                    })

                    # send to users
                    usersInChat = await mongo_chats.find_one({"_id": ObjectId(id_chat)}, {"members": 1})
                    usersInChat = [member["user_id"] for member in usersInChat["members"]]

                    usersNotSent = usersInChat.copy()
                    for user in usersInChat:
                        #if user == token["id_user"]:
                        #    continue
                        #for websock in wsManager.get_active_connections(user):
                        #    await websock.send_text(json.dumps({
                        #        "type": "message_sc",
                        #        "data": {
                        #            "id_chat": id_chat,
                        #            "id_user": token["id_user"],
                        #            "content": message,
                        #            "date": date
                        #        }
                        #    }))
                        for websock in wsManager.get_active_connections(user):
                            await websock.send_text(json.dumps({
                                "type": "new_message",
                            }))
                            if user in usersNotSent:
                                usersNotSent.remove(user)
                    
                    for user in usersNotSent:
                        # update chats -> members -> unread_messages
                        await mongo_chats.update_one({"_id": ObjectId(id_chat), "members.user_id": user}, {"$inc": {"members.$.unread_messages": 1}})

                        
            except Exception as e:
                print(e)
                pass
    except:
        wsManager.disconnect(websocket)
