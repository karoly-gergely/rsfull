import { createRouter, createWebHistory } from 'vue-router'
import store from "../store";
import Home from '../views/Home.vue'
import Login from "../views/Login.vue";

const routes = [
  {
    path: '/',
    name: 'Home',
    component: Home,
  },
  {
    path: '/login',
    name: 'Login',
    component: Login,
  },
  {
    path: '/about',
    name: 'About',
    // route level code-splitting
    // this generates a separate chunk (about.[hash].js) for this route
    // which is lazy-loaded when the route is visited.
    component: () => import(/* webpackChunkName: "about" */ '../views/About.vue'),
  },
]

const router = createRouter({
  history: createWebHistory(),
  routes,
})

router.beforeEach(async (to, from) => {
  const authState = store.state.auth.status;

  if (
    // make sure the user is authenticated
    !authState.isLoggedIn &&
    // ❗️ Avoid an infinite redirect
    to.name !== 'Login'
  ) {
    // redirect the user to the login page
    return { name: 'Login' }
  } else if (
      authState.isLoggedIn &&
      to.name === 'Login'
  ) {
    return { name: from.name }
  }
})

export default router
