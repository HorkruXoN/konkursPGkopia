import asyncio
import uvicorn
import motor.motor_asyncio

from bson.objectid import ObjectId
from fastapi import FastAPI, Request, File, UploadFile
from fastapi.responses import JSONResponse, FileResponse
from fastapi.middleware.cors import CORSMiddleware

from pydantic import BaseModel, Field, ValidationError

# docelowo config z env
import config.config as config

from routes.login import router as routerLogin
from routes.users import router as routerUsers
from routes.me import router as routerMe
from routes.chats import router as routerChats
from routes.admin import router as routerAdmin
from schemas.global_schema import DefReq
from ftplib import FTP

from websockets_api import router as routerWS
import os

import threading
import time

from database import mongo_users, mongo_chats, mongo_messages

import ldap_sync


# from routes.me import router as routerMe
from schemas.database import User, ChatGroup, ChatUser, Message

USE_DATABASE = False




app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)











app.include_router(routerLogin, tags=["login"], prefix="/login")
app.include_router(routerMe, tags=["me"], prefix="/me")
app.include_router(routerUsers, tags=["users"], prefix="/users")
app.include_router(routerChats, tags=["chats"], prefix="/chats")
app.include_router(routerAdmin, tags=["admin"], prefix="/admin")
# router to websocket
app.include_router(routerWS, tags=["WS"], prefix="/chat")




async def checkLDAPUsers():
    while True:
        ldap_sync.getUsers()
        await asyncio.sleep(60)

# backup

async def backup():
    while True:
        try:
            # backup mongo_users, mongo_chats, mongo_messages
            # export to json
            # save to ftp

            FTP_HOST = config.ftp['host']
            FTP_PORT = config.ftp['port']
            FTP_USERNAME = config.ftp['username']
            FTP_PASSWORD = config.ftp['password']

            ftp = FTP()
            ftp.connect(FTP_HOST, FTP_PORT)
            ftp.login(FTP_USERNAME, FTP_PASSWORD)

            # backup mongo_users
            data = await mongo_users.find().to_list(length=1000)
            with open("mongo_users.json", "w") as file:
                file.write(str(data))
            ftp.storbinary("STOR mongo_users.json", open("mongo_users.json", "rb"))

            # backup mongo_chats
            data = await mongo_chats.find().to_list(length=1000)
            with open("mongo_chats.json", "w") as file:
                file.write(str(data))

            ftp.storbinary("STOR mongo_chats.json", open("mongo_chats.json", "rb"))

            # backup mongo_messages
            data = await mongo_messages.find().to_list(length=1000)
            with open("mongo_messages.json", "w") as file:
                file.write(str(data))

            ftp.storbinary("STOR mongo_messages.json", open("mongo_messages.json", "rb"))

            ftp.quit()
        except:
            pass
    
        await asyncio.sleep(60)





async def startup_event():
    if config.ftp['enabled']:
        asyncio.create_task(backup())
    if config.ldap['enabled']:
        asyncio.create_task(checkLDAPUsers())

@app.on_event("startup")
async def startup():
    await startup_event()

if __name__ == '__main__':

    uvicorn.run(app = "main:app", host='0.0.0.0', port=8000, reload=True)