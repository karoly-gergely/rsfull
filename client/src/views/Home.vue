<template>
  <div class="home">
    <img alt="RS logo" src="../assets/logo.png" class="logo" />
    <HelloWorld msg="Hello World" />
  </div>
</template>

<script>
import { createNamespacedHelpers } from 'vuex'
import HelloWorld from '@/components/HelloWorld.vue'

const { mapState, mapActions } = createNamespacedHelpers('auth')

export default {
  name: 'Home',
  components: {
    HelloWorld,
  },
  computed: {
    ...mapState({
      user: state => state?.user,
      token: state => state?.token,
      isLoggedIn: state => state?.status?.isLoggedIn
    })
  },
  methods: {
    ...mapActions([
      'login',
    ])
  },
  props: {},
  data() {
    return {}
  },
  async created() {
    await this.login({email: 'karoly.gergely@spiderlinked.com', password: 'SpiderLinked123!'});
  },
}
</script>

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