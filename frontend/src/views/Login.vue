<template>
  <div id="field">
    <form @submit.prevent="login" id="formLogin">
      <div class="data">
        <img src="./path2.png" alt="user" class="icons">
        <label for="username" class="opis">Username:</label>
        <input type="text" v-model="username" required>
      </div>
      <div class="data">
        <img src="./path5.png" alt="password" class="icons">
        <label for="password" class="opis">Password:</label>
        <input type="password" v-model="password" required>
      </div>
      <div class="dodaj">
        <button type="submit" id="logowanie">Login</button>
      </div>
      <div class="dodaj">
        <button @click="resetPass()" id="LoginResetPassword">Zresetuj hasło</button>
      </div>
      <div style="clear: both;"></div>
    </form>
    <div v-if="errorMessage">{{ errorMessage }}</div>
  </div>
</template>

<script>
import config from '../config.js';
export default {
  data() {
    return {
      username: '',
      password: '',
      errorMessage: '',
    };
  },
  methods: {
    async login() {
      try {
        const response = await fetch(config.API_URL+'login', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({
            username: this.username,
            password: this.password,
          }),
        });

        if (response.ok) {
          const data = await response.json();
          localStorage.setItem('token', data.token);
          this.$router.push('/');
        } else {
          const errorData = await response.json();
          this.errorMessage = errorData.message;
        }
      } catch (error) {
        this.errorMessage = 'Błędna nazwa użytkownika lub hasło';
      }
    },
    resetPass() {
            router.push('/resetPassword')
        }
  },
};
</script>


<style>
  #formLogin{
    animation: move 1.5s ;
  }

  @keyframes move {
        0% {
            transform: translateY(-100%);
        }
        100% {
            transform: translateY(0);
        }
    }

  #formLogin input{
    background-color: var(--extraColor);
    border: none;
    color: var(--textExtraColor);
    margin-left: 25px;
    padding: 8px;
    border-radius: 20px;
    width: 30%;
    height: 20px;
  }

  #logowanie{
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

  #LoginResetPassword{
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

  @media only screen and (max-width: 1000px) {
    #formLogin input{
      font-size: 80%;
      width: 50%;
    }
  }
</style>