<template>
    <div id="banerP">
        <img src="./path7.png" alt="options">
        <span>Spersonalizuj swój chat</span> <br>  
        <select name="koloryWybór" id="SColors" @change="changeTheme">
            <option value="rgb(122,186,255);rgb(17,84,156);black;white">Bezchmurne niebo</option>
            <option value="#fafae7;#eba49c;black;white">Łososiowy staw</option>
            <option value="#5ea037;#034b0a;black;white">Świerkowy las</option>
            <option value="#edbacd;#880f3b;black;white">Wiśniowy sad</option>
            <option value="yellow;black;#8080FF;yellow">Dla słabowidzących</option>
        </select>
    </div>
    <div id="banerS">
        <h1>Dodawanie użytkownika</h1>
        
    </div>
    <div id="banerL">
        <button @click="logout()">Wyloguj się</button>
    </div>
    <form @submit.prevent="submitAdd" id="formAdmin">
        <div class="data"><img src="./path4.png" alt="cloud" class="icons"><label class="opis">Nazwa użytkownika</label> <input type="text" required v-model="username"></div>
        <div class="data"><img src="./path2.png" alt="user" class="icons"><label class="opis">Imię</label> <input type="text" required v-model="name"></div>
        <div class="data"><img src="./path2.png" alt="user" class="icons"><label class="opis">Nazwisko</label> <input type="text" required v-model="surname"></div>
        <div class="data"><img src="./path3.png" alt="mail" class="icons"><label class="opis">E-mail</label><input type="email" required v-model="email"></div>
        <!--<div style="clear: both;"></div>-->
        <div class="dodaj"><input id="special" type="submit" value="Dodaj"></div>
    </form>
</template>

<script>
import router from '@/router';
import config from '../config.js';
export default {
  data() {
    return {
      username: '',
      name: '',
      surname: '',
      email: '',
    };
  },
  methods: {
    async submitAdd() {
        const formData = new FormData();
      
        formData.append('req', JSON.stringify({
            "token": localStorage.getItem('token'),
            "username": this.username,
            "email": this.email,
            "name": this.name,
            "surname": this.surname,
        }))

        try {
            const response = await fetch(config.API_URL+'admin/createUser', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: formData,
            });

            if (response.ok) {
            // Handle success
                console.log('Request sent successfully');
            } else {
            // Handle error
                console.error('Request failed');
            }
        } catch (error) {
            console.error('Error:', error);
        }
    },
    handleFileChange(event) {
      this.file = event.target.files[0];
    },
    changeTheme() {
            let value = document.getElementById("SColors").value;
            value = value.split(';')
            document.documentElement.style.setProperty('--mainColor', value[0]);
            document.documentElement.style.setProperty('--extraColor', value[1]);
            document.documentElement.style.setProperty('--textMainColor', value[2]);
            document.documentElement.style.setProperty('--textExtraColor', value[3]);
    },
    logout() {
        localStorage.clear()
        router.push('/login')
    },
  },
};

</script>

<style>
    body{
        margin: 0;
        padding: 0;
        color: var(--textMainColor);
    }
    :root{
        --mainColor: rgb(122,186,255);
        --extraColor: rgb(17,84,156);
        --textMainColor: black;
        --textExtraColor: white;
    }

    #banerS, #banerP, #banerL{
        float: left;
    }

    #banerS{
        width: 57%;
    }

    #banerL{
        width: 20%; 
        text-align: right;
    }

    #banerL button{
        background-color: var(--extraColor);
        border: none;
        color: var(--textExtraColor);
        padding: 8px;
        width: 30%;
        border-radius: 20px;
    }

    #banerP{
        width: 20%;
        background-color: var(--mainColor);
        margin: 1%;
        padding: 4px;
        transform: translateX(-80%);
        transition: transform 2s;
    }

    #banerP:hover{
        transform: translateX(0);
        transition: transform 1.5s;
    }
    
    #banerP img{
        width: 12%;
        float: right;
        padding: 0;
        margin: 3px;
    }

    #banerP input{
        margin: 2px;
    }

    .data{
        display: flex;
        /*justify-content: center;*/
        align-items: center;
        background-color: var(--mainColor);
        float: left;
        width: 54%;
        margin: 10px 23%;
        padding: 10px 5px 10px 5px;
        border-radius: 25px;
        border: 2px black solid;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
    }

    .opis{
        text-transform: capitalize;
        letter-spacing: 1px;
        display: inline-block;
        width: 20%;
        font-weight: bold;
    }

    .data label, .data input {
        margin-top: 0;
        margin-bottom: 0;
    }

    #formAdmin input:not([type="submit"]){
        background-color: var(--extraColor);
        border: none;
        color: var(--textExtraColor);
        margin-left: 25px;
        padding: 8px;
        border-radius: 20px;
        width: 30%;
        height: 20px;
    }

    input[type="text"], input[type="email"], input[type="password"]{
        font-size: 18px;
    }
    
    .dodaj{
        width: 42%;
        margin: 10px 29%;
        border-radius: 25px;
        background-color: var(--extraColor);
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
        float: left;
    }

    #special{
        text-align: center;
        font-weight: bold;
        font-size: 110%;
        text-transform: uppercase;
        color: var(--textExtraColor);
        margin: 10px;
        padding: 1px;
        height: 30px;
        width: 40%;
        border-radius: 20px;
        background-color: var(--extraColor);
        border: none;
    }

    #special:hover{
        cursor: pointer;
    }

    .icons{
        width: 4%;
        margin-left: 5px;
        margin-right: 23%;
    }

    #banerS h1{
        color: var(--extraColor);
        margin: 20px 0 10px 0;
    }

    @media only screen and (max-width: 1500px) {
        #banerP img{
            width: 16%;
        }
    }

    @media only screen and (max-width: 1200px) {
        #banerP{
            width: 25%;
        }

        #banerS{
            width: 48%;

        }

        #banerL{
            width: 24%;
        }

        #banerP img{
            width: 15%;
        }
    }

    /* Css dla urządzeń mobilnych */
    @media only screen and (max-width: 1000px) {
        #formAdmin input:not([type="submit"]){
            width: 60%;
        }
        #banerP img, .icons{
            display: none;
        }
        #banerP{
            transform: translateX(0);
            width: 100%;
        }
        #banerS{
            width: 100%;
        }
        #banerL{
            width: 100%;
            text-align: center;
        }
        #formAdmin input{
            font-size: 80%;
            width: 50%;
        }
        .special{
            font-size: 80%;
        }
        .data{
            width: 80%;
            margin: 2px 10%;
        }
        .opis{
            font-size: 80%;
            width: 50%;
            text-align: left;
        }
    }   
</style>
