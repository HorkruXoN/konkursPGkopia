import { createRouter, createWebHistory } from 'vue-router'
import { ref } from 'vue'
import HomeView from '../views/HomeView.vue'
import Admin from '../views/Admin.vue'
import MessagesView from '../views/MessagesView.vue'
import AllMessagesView from '../views/AllMessagesView.vue'
import Login from '../views/Login.vue'
import NotFound from '../views/NotFound.vue'
import ResetPassword from '../views/ResetPassword.vue'
import ChangePassword from '../views/ChangePassword.vue'
import CreateChat from '../views/CreateChat.vue'
import autoFetchUserData from '@/scripts/getUsers.js';
import getMe from '@/scripts/getMe.js'

const routes = [
  {
    path: '/',
    name: 'home',
    component: HomeView,
    beforeEnter: async (to, from, next) => {
      if (!localStorage.getItem('token')) {
        next('/login');
      } else {
        try {
          let response = await fetch('/api/me', {
            method: 'POST',
            body: JSON.stringify({ 'token': localStorage.getItem('token') }),
            headers: {
              "Accept": "application/json",
              "Content-Type": "application/json"
            }
          });
  
          if (!response.ok) {
            throw Error('fetching data error');
          }
  
          var resp = await response.json();
  
          // Assuming there is at least one chat
          const firstChatId = resp.chats[0].id_chat;
  
          // Redirect to /messages/ with the firstChatId as a parameter
          next({ path: `/messages/${firstChatId}` });
        } catch (err) {
          console.error(err);
          next(); // Continue to the home page if there's an error
        }
      }
    }
  },
  
  {
    path: '/admin',
    name: 'admin',
    component: Admin
  },
  {
    path: '/resetpassword',
    name: 'resetpassword',
    component: ResetPassword
  },
  {
    path: '/createchat',
    name: 'createchat',
    component: CreateChat
  },
  {
    path: '/changepassword/:reset_token',
    name: 'changepassword',
    component: ChangePassword
  },
  {
    path: '/:catchAll(.*)',
    name: 'Not Found',
    component: NotFound,
    beforeEnter: (to, from, next) => {
      next('/')
    }
  },
  {
    path: '/messages/:id_chat',
    name: 'messages',
    component: MessagesView,
    beforeEnter: async (to, from, next) => {
      
      if (!localStorage.getItem('token')) {
        await next('/login');
      } else {
        const userDataFetcher = autoFetchUserData();

        // Start the autoFetch interval
        userDataFetcher.startAutoFetch();

        next();
      }
    },
    props: true
  },
  {
    path: '/allmessages/:id_chat',
    name: 'allmessages',
    component: AllMessagesView,
    beforeEnter: async (to, from, next) => {
      
      if (!localStorage.getItem('token')) {
        await next('/login');
      } else {
        const userDataFetcher = autoFetchUserData();

        // Start the autoFetch interval
        userDataFetcher.startAutoFetch();

        next();
      }
    },
    props: true
  },
  {
    path: '/login',
    name: 'login',
    component: Login,
    beforeEnter: (to, from, next) => {
      if (localStorage.getItem('token')) {
        next('/');
      } else {
        next();
      }
    }
  }

]

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes
})

export default router
