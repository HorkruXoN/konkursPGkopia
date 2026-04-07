<template>
    <div class="chat-list">
        <div v-if="error">{{ error }}</div>
        <div v-else>
            <div v-for="chat in chats" :key="chat.id">
                <!-- <router-link :to="{ name: 'Messages', params: {id: chat.id}} "> -->
                    <ChatTile :chat="chat" />
                <!-- </router-link> -->
            </div>
        </div>
    </div>

</template>

<script>
import getChatList from '../scripts/getChatList.js'
import ChatTile from './chatListSub/ChatTile.vue'

export default {
    components: {ChatTile},
    setup() {
        const {chats, error, load} = getChatList()

        load()      

        return { chats, error}
    }
}
</script>

<style>
a {
    color: white;
    text-decoration: none;
}
</style>