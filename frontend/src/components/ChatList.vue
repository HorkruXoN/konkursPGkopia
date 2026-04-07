<template>
    <div><router-link to="/createchat">Utwórz czat</router-link></div>
    <div v-for="chat in chats.chats" :key="chat.id_chat" class="singleChat">
        <router-link :to="{ name: 'messages', params: {id_chat:chat.id_chat}}" @click="showMessages()"><div class="helpCurrentUser"><SingleChat :chat="chat" :id_user="id_user" :class="{ active: chat.id_chat == active }"/></div></router-link>
    </div>
</template>

<script>
import SingleChat from './SingleChat.vue';
import {ref} from 'vue'
export default {
    components: {SingleChat},
    props: ['chats', 'id_user', 'active'],
    emits: ['showMessages'],
    methods: {
        showMessages() {
            this.$emit('showMessages')
        }
    }

}
</script>