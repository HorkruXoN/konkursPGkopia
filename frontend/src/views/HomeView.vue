<template>
  <div class="home">
    <Navigation />
    <!-- <div v-if="error">{{ error }}</div>
    <div v-else>
      <ChatList :chats="resp" :id_user="id_user" />
    </div> -->
    <Messages />
  </div>
</template>

<script>
import { onMounted } from 'vue';
import ChatList from '@/components/ChatList.vue';
import Navigation from '@/components/Navigation.vue';
import Messages from '@/components/Messages.vue';
import autoFetchUserData from '@/scripts/getUsers.js';
import config from '../config.js';
export default {
  name: 'HomeView',
  components: {
    Navigation,
    ChatList,
    Messages,
  },
  setup() {
    const { id_user, startAutoFetch } = autoFetchUserData();

    onMounted(() => {
      startAutoFetch();
    });

    return { id_user };
  },
};
</script>
