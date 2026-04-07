<template>
  <div id="field">
    <form @submit.prevent="changePassword" id="formChange">
      <div class="dataV2">
        <div>
        <img src="./path5.png" alt="password" class="icons">
        </div>
        <div>
        <label for="password">Nowe hasło:</label> <br>
        <input type="password" v-model="password" required>
        </div>
      </div>
      <div class="dataV2">
        <div>
        <img src="./path5.png" alt="password" class="icons">
        </div>
        <div>
        <label for="password">Powtórz nowe hasło:</label> <br>
        <input type="password" v-model="password2" required>
        </div>
      </div>
      <div class="dodaj">
        <button type="submit" id="zmianaHasla">Zmień hasło</button>
      </div>
      <div style="clear: both;"></div>
    </form>
    <div v-if="successMessage">{{ successMessage }}</div>
    <div v-if="errorMessage">{{ errorMessage }}</div>
  </div>
</template>

<style>
  .dataV2{
    display: block;
    float: left;
    width: 54%;
    margin: 10px 23%;
    border: 2px black solid;
    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
    border-radius: 25px;
    background-color: var(--mainColor);
  }

  .dataV2 div{
    float: left;
  }

  .dataV2 div:first-child{
    width: 30%;
  }

  .dataV2 div:last-child{
    margin-top: 10px;
    width: 40%;
    text-align: center;
  }

  .dataV2 label{
    width: 100%;
    text-transform: capitalize;
    font-weight: bold;
    letter-spacing: 1px;
  }

  .dataV2 input{
    width: 80%;
    margin: 10px 0 10px 0;
  }

  .dataV2 img{
    width: 20%;
    margin: 10px 10px 0px 5px;
    float: left;
  }

  #formChange {
    animation: move 1.5s;
  }

  @keyframes move {
    0% {
      transform: translateY(-100%);
    }
    100% {
      transform: translateY(0);
    }
  }

  #formChange input {
    background-color: var(--extraColor);
    border: none;
    color: white;
    padding: 8px;
    border-radius: 20px;
    height: 20px;
  }

  #zmianaHasla {
    text-align: center;
    font-weight: bold;
    text-transform: uppercase;
    color: white;
    margin: 10px;
    padding: 1px;
    height: 30px;
    width: 40%;
    border-radius: 20px;
    background-color: var(--extraColor);
    border: none;
  }

  @media only screen and (max-width: 1000px) {
    #formChange div:last-child{
      width: 80%;
      margin-left: 10%;
    }
  }
</style>

<script>
import config from '../config.js';
export default {
  
  props: ['reset_token'],
  data() {
    return {
      password: '',
      password2: '',
      successMessage: null,
      errorMessage: null,
    };
  },
  methods: {
    async changePassword() {
      // Check if passwords match
      if (this.password !== this.password2) {
        this.errorMessage = 'Hasła nie są takie same';
        this.successMessage = null;
        return;
      }

      try {
        const response = await fetch(config.API_URL+'changePassword', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({
            reset_token: this.reset_token,
            new_password: this.password,
          }),
        });

        if (response.ok) {
          this.successMessage = 'Hasło zostało pomyślnie zmienione';
          this.errorMessage = null;
        } else {
          const responseData = await response.json();
          this.successMessage = null;
          this.errorMessage = responseData.message || 'Błąd autoryzacji, spróbuj jeszcze raz';
        }
      } catch (error) {
        console.error('Error during API request:', error);
        this.successMessage = null;
        this.errorMessage = 'Błąd autoryzacji, spróbuj jeszcze raz';
      }
    },
  },
};
</script>
