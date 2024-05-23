<script>
import { createNamespacedHelpers } from 'vuex'
import LoginForm from '@/components/LoginForm.vue'

const { mapState, mapActions } = createNamespacedHelpers('auth')

export default {
  name: 'Login',
  components: {
    LoginForm,
  },
  computed: {
    ...mapState({
      user: state => state?.user,
      token: state => state?.token,
      isLoggedIn: state => state?.status?.isLoggedIn
    }),
  },
  methods: {
    ...mapActions([
      'login',
    ]),
    loginUser: async function(data) {
      try {
        await this.login({...data});
        if (this.isLoggedIn) {
          this.$router.push({path: "/"});
        }
      } catch (e) {
        this.errorMessage = "Incorrect email and password combination"
      }
    }
  },
  data() {
    return {
      errorMessage: ''
    }
  },
  props: {},
}
</script>

<template>
  <div class="home">
    <img alt="RS logo" src="../assets/logo.png" class="logo" />
    <LoginForm @handleSubmit="loginUser" :error="errorMessage"/>
  </div>
</template>

<style scoped>
.logo {
  height: 6em;
  padding: 1.5em;
  will-change: filter;
  transition: filter 300ms;
}
.logo:hover {
  filter: drop-shadow(0 0 2em #646cffaa);
}
.logo.vue:hover {
  filter: drop-shadow(0 0 2em #42b883aa);
}
</style>