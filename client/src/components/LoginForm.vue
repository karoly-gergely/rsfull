<script setup>
import { ref } from 'vue'

defineProps({
    error: String
});

const emit = defineEmits(['handleSubmit']);
const credentials = ref({
  email: '',
  password: ''
});

function onSubmit(e) {
  e.preventDefault();
  emit('handleSubmit', credentials.value);
}
</script>

<template>
  <h1>Please Login Below</h1>

  <div class="login-page">
    <div class="form" @submit="onSubmit">
      <form class="login-form">
        <input type="text" placeholder="username" v-model="credentials.email"/>
        <input type="password" placeholder="password" v-model="credentials.password"/>
        <p class="error">{{error}}</p>
        <button @click="onSubmit">login</button>
      </form>
    </div>
  </div>
</template>

<style scoped>
.login-page {
  width: 360px;
  padding: 8% 0 0;
  margin: auto;
}
.form {
  position: relative;
  border-radius: 8px;
  z-index: 1;
  background: #242424;
  max-width: 360px;
  margin: 0 auto 100px;
  padding: 45px;
  text-align: center;
  box-shadow: 0 0 20px 0 rgba(0, 0, 0, 0.2), 0 5px 5px 0 rgba(0, 0, 0, 0.24);
}
.form input {
  font-family: "Roboto", sans-serif;
  outline: 0;
  background: rgb(28, 28, 28);
  width: 100%;
  border: 0;
  margin: 0 0 15px;
  padding: 15px;
  box-sizing: border-box;
  font-size: 14px;
}
.form button {
  font-family: "Roboto", sans-serif;
  text-transform: uppercase;
  outline: 0;
  background: #2c3e50;
  width: 100%;
  border: 0;
  padding: 15px;
  color: #FFFFFF;
  font-size: 14px;
  -webkit-transition: all 0.3 ease;
  transition: all 0.3 ease;
  cursor: pointer;
}
.form button:hover,.form button:active,.form button:focus {
  filter: opacity(0.75);
}

.form p.error {
  color: red;
  margin-top: 0;
  font-size: 0.75rem;
}
</style>
