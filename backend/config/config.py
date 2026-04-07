ldap = {
    "enabled": False, # "True" to enable LDAP
    "server": "10.0.99.111",
    "domain": "PG",
    "username": "Andrzej",
    "password": "abc123!@#",
}

db = {
    "host": "mongodb", # mongodb
    "port": 27017,
    "username": "",
    "password": "",
}

JWT_SECRET = "6e227da48a015fc6d4ba4af946c9b0010ffd52f94ababb2a"

email = {
    "host": "mail.srv",
    "port": 25,
    "username": "",
    "password": "",
    "from": "chatpg@pg.pl"
}

ftp = {
    "enabled": False, # "True" to enable FTP
    "host": "10.0.100.3",
    "port": 2121,
    "username": "testuser",
    "password": "testpassword"
}