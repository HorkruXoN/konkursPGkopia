**/login**
 - reset password
 - logout (localstorage.clear()) + window.reload()

**/**

**/admin**

**/{id_chat}/messages** (/chats/{id_chat}/messagesAll)
  - 
  ```
    {
        "token": token(string z local storage) 
            [localstorage.getItem('token')]
    }
  ```
  - response
  ```
    {
        [{
            "id_user":
            "content":
            "date":
        }]
    }
  ```

**/chats/createChat**
  - request: 
  ```
    {
        "token": token(string z local storage) 
            [localstorage.getItem('token')]
        "type": group/user 
        "name": string //jeśli jest >2 osób wybranych (czat grupowy)
    }
  ```
  - return:
  ```
  {
    "id_chat": "string",
    "is_group": true,
    "members": [
        "string"
    ],
    "name": "string",
    "admin": "string"
  }
  ```
**/chats/addUser**
  - request: 
  ```
    {
        "token": token(string z local storage) 
            [localstorage.getItem('token')]
        "id_chat": 
        "members": [] //tylko dodawani
    }
  ```

**/login/setpassword**
  - request
  ```
  {
    "passwordToken":
    "password":
  }
  ```