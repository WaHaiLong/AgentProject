import { createRouter, createWebHistory } from 'vue-router'
import Login from '../views/Login.vue'
import Home from '../views/Home.vue'
import FormPage from '../views/FormPage.vue'

const routes = [
  {
    path: '/',
    redirect: '/login'
  },
  {
    path: '/login',
    name: 'Login',
    component: Login
  },
  {
    path: '/home',
    name: 'Home',
    component: Home
  },
  {
    path: '/form',
    name: 'FormPage',
    component: FormPage
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router