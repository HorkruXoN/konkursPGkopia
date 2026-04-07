# KONCEPT STRUKTURY FRONTENDU

**GŁÓWNA STRONA**
1. Strona z logowaniem, jeśli jest niezalogowany ( LoginView.vue )

LUB

2. MainView.vue
   - widok zawierający komponenty:
       - Navigation.vue
         - skróty do czatów ( Favourite.vue - jako router link do Messages.vue z id = id czatu )
         - na dole przełącznik tryb jasny/ciemny ( oraz wysoki kontrast ?)
       - ChatList.vue
         - Chat.vue ( komponent zawierający pojedynczy czat: { zdjęcie, imię i nazwisko (nick), ostatnia wiadomość, aktywność (jeśli offline to kiedy) } )
         - jako router link do Messages.vue z id = id czatu
       - Messages.vue
         - Message.vue ( komponent zawierający pojedynczą wiadomość: { autor, treść, czas wysłania, kto odczytał } )