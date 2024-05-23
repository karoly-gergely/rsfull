<script setup>
import store from "./store";

const authState = store.state.auth.status;
</script>

<template>
  <div id="nav" v-if="authState?.isLoggedIn">
    <router-link to="/">Home</router-link> |
    <router-link to="/about">About</router-link>
  </div>
  <router-view />

</template>

