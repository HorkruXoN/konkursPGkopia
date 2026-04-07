import sys
from ldap3 import Server, Connection, ALL, NTLM, ALL_ATTRIBUTES, ALL_OPERATIONAL_ATTRIBUTES, AUTO_BIND_NO_TLS, SUBTREE
from ldap3.core.exceptions import LDAPCursorError
import config.config as config
import random
import string
import smtplib

from database import mongo_users



async def getUsers():
    server = Server(config.ldap['server'], get_info=ALL)
    conn = Connection(server, user='{}\\{}'.format(config.ldap['domain'], config.ldap['username']), password=config.ldap['password'], authentication=NTLM, auto_bind=True)

    # objectclass=person and name=*
    # cn=Users
    conn.search('dc={},dc=local'.format(config.ldap['domain']), '(objectclass=person)', attributes=[ALL_ATTRIBUTES, ALL_OPERATIONAL_ATTRIBUTES])

    for e in conn.entries:
        # if is not user
        if e['logonCount'].value == 0:
            continue


        username = e['sAMAccountName'].value
        full_name = e['name'].value
        email = e['mail'].value if 'mail' in e else None

        # check if user exists
        user = await mongo_users.find_one({"username": username})
        if user:
            continue

        # add user to db
        password = ''.join(random.choice(string.ascii_letters + string.digits) for i in range(10))
        await mongo_users.insert_one({
            "username": username,
            "full_name": full_name,
            "email": email,
            "password": password,
            "salt": "",
            "is_active": False,
            "last_seen": "1900-01-01T00:00:00Z",
        })

        # send email
        if email:
            message = 'Subject: {}\n\n{}'.format('Witaj na czacie firmowym!', 'Twoje nowe haslo to: {}. Zmien je jak najszybcej!'.format(password))
            server = smtplib.SMTP('localhost', 1025)
            #server.login('','')
            server.sendmail("chattest@example.com", email, message)
            server.quit()
            print('Email sent to {}'.format(email))
        
    return True


    conn.unbind()