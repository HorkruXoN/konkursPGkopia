<template>
    <form @submit.prevent="createChat()" id="createChat">
        <!--wyszukiwarka-->
        <table>
        <div v-for="user in users" class="user">
            <tr>
            <td><label><input type="checkbox" :value="user.id_user" @change="handleEdit()" class="userCheck">{{ user.full_name }}</label></td>
            </tr>
        </div>
        </table>
        <div v-if="isGroup"><label>Nazwa grupy: </label><input type='text' v-model="name" required></div>
        <input type="submit" v-if="ready" value="Utwórz czat">
        
    </form>
</template>

<style>
    #createChat table{
        width: 100%;
        text-align: center;
    }

    #createChat div{
        display: block;
        width: 80%;
        margin: 5px auto;
        border-radius: 10px;
        background-color: var(--extraColor);
        color: var(--textExtraColor);
        border: 2px solid var(--mainColor);
        padding: 4px;
    }

    #createChat input[type="submit"]{
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
        border: 2px solid var(--mainColor);
    }

    #createChat input[type="text"]{
        width: 40%;
        background-color: var(--mainColor);
        border: none;
        border-radius: 20px;
    }

    @media screen and (max-width: 1000px){
        #createChat input[type="submit"]{
            font-size: 100%;
            font-weight: normal;
            text-transform: none;
        }

        #createChat input[type="text"]{
            width: 80%;
        }
    }
</style>

<script>
import router from '@/router';
import autoFetchUserData from '@/scripts/getUsers.js';
import { ref } from 'vue'
import config from '../config.js';
export default {
    setup() {
        const userDataFetcher = autoFetchUserData();
        userDataFetcher.startAutoFetch();
        const users = ref(JSON.parse(localStorage.getItem('users')).users)
        const isGroup = ref(false)
        const members = ref([])
        const name = ref('')
        const ready = ref(false)
        return { users, isGroup, members, name, ready }
    },
    methods: {
        handleEdit() {
            const checkboxes = document.getElementsByClassName("userCheck")
            this.members = []
            for (let i = 0; i < checkboxes.length; i++) {
                if (checkboxes[i].checked) {
                    this.members.push(checkboxes[i].value)
                }
            }
            if (this.members.length > 1) {
                this.isGroup = true
            } else if (this.members.length > 0) {
                this.isGroup = false
                this.ready = true
                this.name = ''
            } else {
                this.isGroup = false
                this.ready = false
                this.name = ''
            }
        },
        async createChat() {
            let type = this.members.length > 1 ? "group" : "user" 
            const requestBody = {
                "token": localStorage.getItem("token"), // Pamiętaj, aby dostarczyć rzeczywisty token
                "type": type, // Pamiętaj, aby dostarczyć rzeczywisty typ
                "name": this.isGroup ? this.name : '',
                "members": this.members
            };

            try {
                const response = await fetch(config.API_URL+"chats/createChat", {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify(requestBody),
                });

                if (response.ok) {
                    console.log('Chat created successfully');
                    router.push("/")
                } else {
                    console.error('Error creating chat');
                }
            } catch (error) {
                console.error('Error:', error);
            }
        }
    }
}
</script>
