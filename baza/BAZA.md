# Opis bazy danych

## Tabela Użytkowników
Atrybuty:  
id_user -> identyfikator, "U___", typ danych: String  
name -> typ danych: String  
surname -> typ danych: String  
login -> typ danych: String, musi być to wartość unikatowa  
date -> data urodzenia, typ danych: Date  
e-mail -> typ danych: String, musi być to wartość unikatowa  **BARDZO NIEPOTRZEBNY - usunąłem**
foto -> "nazwa.rozszerzenie" (zdjęcia będzie trzeba pobierać na serwer)  
salt ->  
hashed_password ->  hash(password+salt)  
conversations -> typ danych: Array: [id_group, nick]  
favorite -> przypięte czaty, typ danych: Array: [id_user /id_group]  
is_active -> typ danych: Boolean, TRUE - użytkownik jest aktywny, FALSE - nie jest aktywny  
last_seen -> typ danych: date, data i godzina, kiedy użytkownik był widziany ostatni raz  

### Przykładowy kod
```
db.createCollection("Users",  
    {  
        id_user: "<string>",  
        name: "<string>",  
        surname: "<string>",  
        login: "<string>",  
        date: "<date>",  
        foto: "<string>",  
        salt: "<string>",  
        password: "<string>",  
        conversations: [{  
            id_group: "<string>",  
            nick: "<string>",
            is_favourite: "<bool>",
            unread_messages: "<number>"
        }],  
        is_active: "<boolean>",  
        last_seen: "<date>"  
    }  
)
```

## Tabela grup
Atrybuty:  
id_group -> id konwersacji (jeżeli na początku U-konwersacja 2 użytkowników, G-grupa), typ danych: String  
group_name -> nawa grupy (w przypadku U -> NULL), typ danych: String  
admin -> administrator - id_user (w przypadku U -> NULL), typ danych: String  
new_messages -> przy nowych wiadomościach dodaje się wszystkich użytkowników oprócz autora, typ danych: Array: [id_user, number] (number - liczba nieodczytanych wiadomości - przy dodaniu nowej wiadomości automatycznie zwiększa się o 1, domyślnie 0), rozwiązanie to pozwala nam uniknąć problemu, że przy dodaniu nowego usera do grupy będzie miał mnóstwo nowych nieodczytanych wiadomości  
foto -> zdjęcie grupy (w przypadku U-> NULL), typ danych: String

### Przykładowy kod
```
db.createCollection("Groups",  
    {  
        id_group: "<string>",  
        group_name: "<string>",  
        admin: "<string>",  
        foto: "<string>"  
    }  
)
```

## Tabela wiadomości
Atrybuty:  
id_group -> id konwersacji (jeżeli na początku U-konwersacja 2 użytkowników, G-grupa), typ danych: String  
message -> zawartość wiadomości, typ danych: String  
autor -> id_usera, autor wiadomości, typ danych: String  
date -> data wiadomości, typ danych: Date  

### Przykładowy kod
```
db.createCollection("Messages",  
    {  
        id_group: "<string>",  
        message: "<string>",  
        autor: "<string>",  
        date: "<date>",
        not_read_by: "<list>"
    }  
)
```


### Insert
```
db.Users.insertOne({
    id_user: 'URvaxwLKL7q',
    name: 'Andrzej',
    surname: 'Nowak',
    login: 'Andrej123',
    date: new Date('2004-01-01'),
    foto: 'andrzej.png',
    salt: 'adamek',
    password: '1697903492491045130',
    conversation: [
        {id_group: 'UxsJDdMSc9Y', unerad_messages: 0},
        {id_group: 'GzT8bB9JKwe', nick: 'andrzejek', unerad_messages: 0},
        {id_group: 'UvG0rE13RSm', unread_messages: 0}
    ]
})

db.Users.insertOne({
    id_user: 'ULDOdyYU0QK',
    name: 'Adam',
    surname: 'Janek',
    login: 'Adamek5',
    date: new Date('1985-03-21'),
    foto: 'adam.png',
    salt: 'adamek',
    password: '1697903492491045130',
    conversation: [
        {id_group: 'UxsJDdMSc9Y', unerad_messages: 0},
        {id_group: 'GzT8bB9JKwe', nick: 'adaś', unerad_messages: 0}
    ]
})

db.Users.insertOne({
    id_user: 'UgGmSrNVUWZ',
    name: 'Filip',
    surname: 'Wozniak',
    login: 'LubieMarka',
    date: new Date('2004-10-15'),
    foto: 'quambi.jpg',
    salt: 'adamek',
    password: '1697903492491045130',
    conversation: [
        {id_group: 'GzT8bB9JKwe', nick: 'Mokebe', unerad_messages: 0},
        {id_group: 'UvG0rE13RSm', unread_messages: 0}
    ]
})
```


### InsertMany
```
db.Groups.insertMany(
    [
        {id_group: 'UxsJDdMSc9Y'},
        {id_group: 'GzT8bB9JKwe', group_name: 'Adamki', admin: 'ULDOdyYU0QK', foto: 'kaczki.jpeg'},
        {id_group: 'UvG0rE13RSm'}
    ]
)

db.Messages.insertMany(
    [
        {id_group: 'UxsJDdMSc9Y', message: 'Cześć Andrzej', autor: 'ULDOdyYU0QK', date: new Date(), not_read_by: ['URvaxwLKL7q'] },
        {id_group: 'UxsJDdMSc9Y', message: 'Mój kot Leon chce się z tobą pobawić', autor: 'ULDOdyYU0QK', date: new Date(), not_read_by: ['URvaxwLKL7q'] },
        {id_group: 'GzT8bB9JKwe', message: 'Elo, to grupa moich ziomków', autor: 'ULDOdyYU0QK', date: new Date(), not_read_by: ['URvaxwLKL7q', 'UgGmSrNVUWZ'] },
        {id_group: 'UvG0rE13RSm', message: 'Z Adamem wszystko w porządku?', autor: 'UgGmSrNVUWZ', date: new Date(), not_read_by: ['URvaxwLKL7q'] }
    ]
)
```