import Vue from 'vue'
import Router from 'vue-router'
import Nuchal from '@/views/Nuchal'

Vue.use(Router)

export default new Router({
  routes: [
    { path: '/', name: 'Nuchal', component: Nuchal }
  ]
})
