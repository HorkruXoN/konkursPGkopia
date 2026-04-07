import motor.motor_asyncio
from config.config import db

client = motor.motor_asyncio.AsyncIOMotorClient("mongodb://"+db["host"]+":27017/")
db = client.get_database("kpg")

mongo_users = db.get_collection("Users")
mongo_chats = db.get_collection("Chats")
mongo_messages = db.get_collection("Messages")
mongo_passwd_resets = db.get_collection("PasswdResets")