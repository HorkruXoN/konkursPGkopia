import jwt
from bson import ObjectId

from database import mongo_users
from pydantic import BaseModel, Field
import random
import string
import smtplib
import bcrypt

import config.config as config



def verifyUser(token):
    try:
        return jwt.decode(token, config.JWT_SECRET, algorithms=["HS256"])
    except:
        return None




async def create_user(username: str, email: str, full_name: str):
    # check if user exists by username or email
    user = await mongo_users.find_one({"$or": [{"username": username}, {"email": email}]})
    if user:
        return None

    # add user to db
    password_unhashed = ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(10))
    salt = bcrypt.gensalt()

    #password = hashlib.sha256((password_unhashed + salt).encode()).hexdigest()
    password = bcrypt.hashpw(password_unhashed.encode(), salt)


    res = await mongo_users.insert_one({
        "username": username,
        "full_name": full_name,
        "email": email,
        "password": password.decode(),
        "is_active": False,
        "last_seen": "1900-01-01 00:00:00",
        "is_admin": False,
    })

    # send email
    if False:
        message = 'Subject: {}\n\n{}'.format('Witaj na czacie firmowym!', 'Twoje nowe haslo to: {}. Zmien je jak najszybcej!'.format(password_unhashed))
        server = smtplib.SMTP(config.email['host'], config.email['port'])
        #server.login('','')
        server.sendmail(config.email['from'], email, message)
        server.quit()

    return res.inserted_id
