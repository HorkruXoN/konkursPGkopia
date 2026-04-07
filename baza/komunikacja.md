**WCZYTANIE STRONY**
- /me
    - Zwraca informacje o użytkowniku i jego grupach, czatach, i ostatnich wiadomościach, uczestnikach (bez siebie)!
- /users
    - Zwaca listę użytkowników
    - /{id}
        - Zwraca informacje o użytkowniku, Imie, nazwisko, url zdjęcia
    
- /chats
    - /createChat
        - Tworzenie nowego czatu
        ```json
        {
            "type": "group/user",
            "users": ["id1", "id2"] // bez siebie, dla typu user - lista z jednym elementem
        }
        ```
        zwraca id nowego czatu
    - /{id}
        - /messages_all
            - Zwraca wszystkie wiadomości z czatu => DO HISTORII CZATU
        - /messages
            - Zwraca od momentu ostatniej nieodczytanej wiadomości +10
- /login
    - Logowanie - do zrobienia


**WEBSOCKET**
W PRZYPADKU WEBSOCKET, username i token są wymagane w każdej wiadomości.
- /ws/connect
    - Połączenie z serwerem websocket
- /ws/send
    - Wysłanie wiadomości
    - Wysyłane na websocket w formacie json, typu:
    ```json
    {
        "type": "message_cs",
        "data": {
            "chat_id": "1",
            "message": "Hello world"
        }
    }
    ```
- **ODBIERANIE WIADOMOŚCI**
    - przychodzące na websocket w formacie json, typu:
    ```json
    {
        "type": "message_sc",
        "data": {
            "chat_id": "1",
            "user_id": "1",
            "message": "Hello world",
            "date": "2020-01-01 12:00:00"
        }
    }
    ```

    !!! Jeżeli chat_id jest nieznany, to należy odświeżyć listę czatów.