<template>
  <div id="MainMessages" ref="messagesContainer">
    <SingleMessage v-for="message in messages.messages" :key="message.date" :message="message" />
  </div>
  <div id="messageInput">
    <form @submit.prevent="sendMessage()">
      <textarea ref="messageTextarea" id="messageToSend" @keydown="handleKeyDown"></textarea> <br>
      <input type="submit" value="Wyślij">
    </form>
  </div>
</template>

<script>
import router from '@/router';
import config from '../config.js';
import SingleMessage from './SingleMessage.vue';
import getMe from '@/scripts/getMe.js';

export default {
  props: ['id_chat'],
  emits: ['refresh'],
  data() {
    return {
      messages: [],
      ws: null,
    };
  },
  methods: {
    async fetchMessages() {
      localStorage.removeItem('actualDate');
      try {
        const token = localStorage.getItem('token');
        const response = await fetch(config.API_URL+`chats/${this.id_chat}/messages`, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({ token: token }),
        });
        const data = await response.json();
        this.messages = data; // Update messages with the fetched data
        this.$refs.messagesContainer.scrollTop = this.$refs.messagesContainer.scrollHeight;
      } catch (error) {
        console.error('Error fetching data:', error);
      }
      this.loadData();
    },
    async loadData() {
      const token = localStorage.getItem('token');
      // Call the load method from getMe.js
      getMe().load(token);
    },
    async sendMessage() {
      let messageTextarea = this.$refs.messageTextarea;
      let messageToSend = messageTextarea.value;
      if (messageToSend != '') {
        messageTextarea.value = '';
        const dataToSend = {
          type: 'message',
          data: {
            id_chat: this.id_chat,
            message: messageToSend,
          },
        };
        this.ws.send(JSON.stringify(dataToSend));
        this.fetchMessages();
        this.$emit('refresh');
      }
    },
    handleKeyDown(event) {
      if (event.key === 'Enter' && !event.shiftKey) {
        event.preventDefault();
        this.sendMessage();
      }
    },
  },
  async created() {
    localStorage.removeItem('actualDate');
    try {
      const token = localStorage.getItem('token');
      const response = await fetch(config.API_URL+`chats/${this.id_chat}/messages`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ token: token }),
      });
      const data = await response.json();
      this.messages = data; // Update messages with the fetched data
    } catch (error) {
      console.error('Error fetching data:', error);
    }

    // Call the load method from getMe.js after the component is created
    this.loadData();

    // Check if WebSocket is not already open before creating a new one
    if (!this.ws || this.ws.readyState === WebSocket.CLOSED) {
      this.ws = new WebSocket('wss://'+location.host+'/api/chat/connect/' + localStorage.getItem('token'));
      this.ws.onopen = () => {};
      this.ws.onmessage = (e) => {
        if (JSON.parse(e.data).type == 'new_message') {
          // play audio.mp3
          let audio = new Audio('http://soundbible.com/mp3/Air Plane Ding-SoundBible.com-496729130.mp3');
          audio.play();
          this.fetchMessages();
        }
        this.$emit('refresh');
      };
      this.ws.onclose = () => {
        console.log('Disconnected');
      };
    }
  },
  mounted() {
    // Przewiń do dołu po załadowaniu strony
    localStorage.removeItem('actualDate');
    this.fetchMessages();
  },
  components: { SingleMessage },
};
</script>

<style>
#messageToSend {
  resize: none; /* Zapobiega automatycznemu rozszerzaniu pola tekstowego */
}
</style>
