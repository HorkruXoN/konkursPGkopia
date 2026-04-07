<template>
<div v-if="isFirstDate">{{ message.date.split("T")[0] }}</div>
<div class="message">
        <div class="senderYou" v-if="isSender"> 
            
            <span class="messageContent"> 
                {{ message.content }}&nbsp;
            </span> <br>
            <span class="messageDate">
                {{ date }} 
            </span> 
        </div>
        <div v-else class="anotherUser">
            <span class="sender"> 
                {{ userName }}:
             </span> <br>
            <span class="messageContent">
                {{ message.content }}&nbsp;
            </span> <br>
            <span class="messageDate">
                {{ date }} 
            </span>
        </div>
        
</div>
</template>

<script>
import { computed } from 'vue'
import config from '../config.js';
export default {
    props: ['message'],
    setup(props){
        const isSender = computed(() => {
            return props.message.id_user == localStorage.getItem('id_user')
        })
        const userName = computed(() => {
            // Retrieve the users data from local storage and parse it
            const storedUsers = localStorage.getItem('users');
            const users = JSON.parse(storedUsers).users || [];

            // Assuming props.chat.last_message.id_user is available
            const messageIdUser = props.message.id_user;

            // Initialize the default value
            let matchedUserFullName = 'Unknown User';

            for (const user of users) {
                if (user.id_user === messageIdUser) {
                    matchedUserFullName = user.full_name;
                    break; // Exit the loop once a match is found
                }
            }

            // Return the full_name
            return matchedUserFullName;
        });
        
        const isFirstDate = computed(() => {
            
            if(typeof localStorage.getItem("actualDate") == 'undefined' || localStorage.getItem('actualDate') != props.message.date.split("T")[0]){
                localStorage.setItem("actualDate", props.message.date.split("T")[0])
                return true
            }
            else{
                // console.log(localStorage.getItem("actualDate"))
                return false
            }
                
        })

        const date = computed(() => {
            const localDate = new Date(props.message.date).toLocaleString()
            const newd = localDate.split(', ')[1].split(":")[0] +":"+ localDate.split(', ')[1].split(":")[1]
            return newd
        })

        return {isSender, userName, isFirstDate, date}
    }
}
</script>