<template>
    <div id="field">
      <form @submit.prevent="resetPassword()" id="formReset">
        <div class="data">
        <img src="./path3.png" alt="user" class="icons">
        <label class="opis">E-mail:</label>
        <input type="text" required v-model="email">
        </div>
        <div class="data">
        <img src="./path2.png" alt="user" class="icons">
        <label for="username" class="opis">Username:</label>
        <input type="text" v-model="username" required>
        </div>
        <div class="dodaj">
        <button type="submit" id="resetowanie">Resetuj hasło</button>
        </div>
        <div style="clear: both;"></div>
      </form>
      <div v-if="successMessage">{{ successMessage }}</div>
      <div v-if="errorMessage">{{ errorMessage }}</div>
    </div>
</template>

<style>
  #formReset{
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

  #formReset input{
    background-color: var(--extraColor);
    border: none;
    color: var(--textExtraColor);
    margin-left: 25px;
    padding: 8px;
    border-radius: 20px;
    width: 30%;
    height: 20px;
  }

  #resetowanie{
    text-align: center;
    font-weight: bold;
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
    #formReset input{
      font-size: 80%;
      width: 50%;
    }
  }
</style>
<script>
import config from '../config.js';
export default {
  data() {
    return {
      username: '',
      email: '',
      successMessage: null,
      errorMessage: null,
    };
  },
  methods: {
    async resetPassword() {
      try {
        const response = await fetch(config.API_URL+'resetPassword', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({
            username: this.username,
            email: this.email,
          }),
        });

        if (response.ok) {
          this.successMessage = 'Wysłano link do resetu hasła na adres e-mail';
          this.errorMessage = null;
        } else {
          const responseData = await response.json();
          this.successMessage = null;
          this.errorMessage = responseData.message || 'Błąd autoryzacji, spróbuj jeszcze raz';
        }
      } catch (error) {
        this.successMessage = null;
        this.errorMessage = 'Błąd autoryzacji, spróbuj jeszcze raz';
      }
    },
  },
};
</script>