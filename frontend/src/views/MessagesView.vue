<!-- MessagesView.vue -->

<template>
  <div class="home">
    <Navigation v-if="show"/>
    <div id="banerInfo"><div><input type="button" value="Czaty" @click="showChats()" id="czaty" v-if="!show"></div><div><router-link :to="'/allmessages/'+id_chat" v-if="showMess">HISTORIA WIADOMOŚCI</router-link></div></div>
    <div style="clear: both;"></div>
    <div v-if="error">{{ error }}</div>
    <div v-else id="ChatList" v-if="show">
      <ChatList :chats="resp" :key="key" :activeChat="id_chat" @showMessages="showMessages()"/>
    </div>
    <Messages :id_chat="id_chat" :key="id_chat" @refresh="refresh" v-if="showMess"/>
    
    <div style="clear: both;"></div>
  </div>
</template>

<style>
    .home{
      overflow: hidden;
      height: 100vh;
    }

    #nav{
      height: 5vh;
      background-color: var(--extraColor);
      text-align: left;
      float: left;
      width: 40%;
    }

    #banerInfo{
      color: var(--textExtraColor);
      float: left;
      height: 5vh;
      width: 60%;
      background-color: var(--extraColor);
    }

    #banerInfo div{
      float: left;
      margin-top: 4px;
      text-align: center;
      width: 100%;
    }

    #banerInfo a{
      font-size: 80%;
      text-transform: uppercase;
      border: 1px var(--textExtraColor) solid;
      color: var(--textExtraColor);
      padding: 2px;
    }

    #banerInfo input[type="button"]{
      display: none;
    }

    #nav button{
      margin: 4px 10px 2px 2px;
      background-color: var(--extraColor);
      color: var(--textExtraColor);
      text-transform: uppercase;
      border: 1px solid var(--textExtraColor);
      padding: 3px;
    }

    #nav select{
      margin: 4px 10px 2px 2px;
      padding: 3px;
    }

    #nav input{
      margin: 4px 10px 2px 2px;
      background-color: var(--extraColor);
      color: var(--textExtraColor);
      text-transform: uppercase;
      border: 1px solid var(--textExtraColor);
      padding: 3px;
    }

    .message{
      width: 100%;
      float: left;
    }

    .anotherUser{
      float: left;
      width: 60%;
      margin: 1% 5%;
      background-color: var(--extraColor);
      color: var(--textExtraColor);
    }

    .anotherUser, .senderYou{
      padding: 3px;
      border-radius: 5px;
    }

    .sender{
      float: left;
      margin: 0 5%;
    }

    .senderYou{
      float: right;
      width: 60%;
      margin: 1% 5%;
      background-color: var(--extraColor);
      color: var(--textExtraColor);
    }

    #ChatList{
      width: 40%;
      float: left;
      overflow-y: auto;
      height: 95vh;
      background-color: var(--extraColor);
    }

    #ChatList a[href="/createchat"]{
      font-size: 80%;
      text-transform: uppercase;
      border: 1px var(--textExtraColor) solid;
      color: var(--textExtraColor);
      padding: 2px;
    }

    #ChatList div:not([class]){
      display: block;
      padding: 4px 0px;
    }

    #MainMessages{
      border-top: 1px solid var(--extraColor);
      border-bottom: 1px solid var(--extraColor);
      background-color: var(--mainColor);
      overflow-y: auto;
      float: left;
      width: 60%;
      height: 75vh;
    }

    #MainMessages div:not([class]){
      color: var(--textMainColor);
      margin: 4px;
      font-weight: bold;
    }

    #messageInput{
      border-top: 4px solid var(--extraColor);
      float: left;
      width: 60%;
      padding: 20px 0;
      background-color: var(--mainColor);
      height: 20vh;
    }

    #messageInput textarea{
      max-width: 80%;
      width: 80%;
      color: var(--textExtraColor);
      background-color: var(--extraColor);
      max-height: 10vh;
    }

    #messageInput input{
      margin: 2px;
      background-color: var(--extraColor);
      color: var(--textExtraColor);
      text-transform: uppercase;
      border: 1px solid var(--textExtraColor);
      padding: 10px 20px;
    }

    a{
      text-decoration: none;
      color: var(--textMainColor);
    }

    .singleChat{
      display: block;
      border: 2px solid var(--extraColor);
      background-color: var(--mainColor);
    }

    .messageDate{
      float: right;
      /*display: none;*/
    }

    .userFoto, .info{
      float: left;
    }

    .userFoto{
      width: 30%;
      text-align: center;
    }

    .info{
      width: 70%;
    }

    .userFoto img{
      border-radius: 50%;
      width: 40%;
      margin: 2px;
    }

    .chatName{
      font-weight: bold;
    }

    .lastMessage{
      float: left;
      text-align: left;
      width: 60%;
      overflow: hidden;
      white-space: nowrap;
      text-overflow: ellipsis;
    }

    .lastMessageDate{
      width: 30%;
      float: right;
      text-align: right;
      padding-right: 2px;
    }

    .offlineStatus{
      font-size: 80%;
    }

    .activeStatus{
      font-size: 80%;
      color: #034b0a;
      font-weight: bold;
    }

    .router-link-active div{
      background-color: var(--extraColor);
      color: var(--textExtraColor);
    }

    .router-link-active .helpCurrentUser{
      border: 1px solid var(--textExtraColor);
    }

    @media screen and (max-width: 1400px) {
      .userFoto img{
        width: 60%;
      }
    }

    @media screen and (max-width: 1100px) {
      /* #ChatList{
        display: none;
      } */
      
      #banerInfo{
        width: 100%;
      }
      #MainMessages{
        width: 100%;
      }
      #messageInput{
        width: 100%;
      }
      #banerInfo div{
        width: 60%;
        float: left;
        margin-top: 4px;
      }
      #banerInfo div:first-child{
        width: 20%;
      }
      #banerInfo input[type="button"]{
        display: block;
        font-size: 80%;
        text-transform: uppercase;
        border: 1px var(--textExtraColor) solid;
        color: var(--textExtraColor);
        padding: 2px;
        background-color: var(--extraColor);
      }
      /* .messageDate{
        font-size: 80%;
      } */
      /*#banerInfo{
        display: none;
      }
      #MainMessages{
        display: none;
      }
      #messageInput{
        display: none;
      }*/
      /* #ChatList{
        width: 100%;
      }
      #nav{
        width: 100%;
      }
      .lastMessageDate{
        font-size: 80%;
      }
      #nav select{
        width: 30%;
      }
      #nav input{
        width: 30%;
      }
      .lastMessage{
        font-size: 90%;
      } */
      
    }
</style>

<script>
import { ref, onMounted, watch, getCurrentInstance } from 'vue';
import { useRouter } from 'vue-router';
import ChatList from '@/components/ChatList.vue';
import Navigation from '@/components/Navigation.vue';
import Messages from '@/components/Messages.vue';
import getMe from '@/scripts/getMe.js';
import autoFetchUserData from '@/scripts/getUsers.js';
import config from '../config.js';
const key = ref(0)
export default {
  name: 'HomeView',
  props: ['id_chat'],
  components: {
    Navigation,
    ChatList,
    Messages,
  },
  setup(props) {
    const router = useRouter();
    const { resp, error, load } = getMe();
    const { id_user, startAutoFetch } = autoFetchUserData();
    const show = ref(true)
    const showMess = ref(true)
    onMounted(() => {
      startAutoFetch();
      load(id_user.value);
      handleMediaChange()
    });

    const refresh = async () => {
      try {
        await load(id_user.value); // Reload data using getMe
        key.value++; // Increment key to force re-render of ChatList
      } catch (error) {
        console.error('Error refreshing data:', error);
      }
    };
    
    const media = window.matchMedia("(max-width: 1100px)");

    const handleMediaChange = () => {
      if (media.matches) {
        show.value = false;
        showMess.value = true;
        
      } else {
        // Adjust behavior for larger screens if needed
        show.value = true;
        showMess.value = true;
      }
    };

// Watch for changes in screen width
    watch(() => media.matches, handleMediaChange);

    // Initial check on component mount
    handleMediaChange();

  

    return { resp, error, id_user, refresh, key, show, showMess, handleMediaChange};
  },
  methods: {
    showChats() {
      let media = window.matchMedia("(max-width: 1100px)")
      if(media.matches)
      {
        this.show = true
        this.showMess = false
      }
    },
    showMessages()
    {
      let media = window.matchMedia("(max-width: 1100px)")
      if(media.matches)
      {
        this.show = false
        this.showMess = true
      }
    },
    
  },
  created() {
        window.addEventListener('resize', this.handleMediaChange);
      },
      destroyed() {
        window.removeEventListener('resize', this.handleMediaChange);
      },
};
</script>
