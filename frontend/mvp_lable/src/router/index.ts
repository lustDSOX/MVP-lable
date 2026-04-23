
import CaseDetail from '@/components/cases/CaseDetail.vue'
import GuideDetail from '@/components/guides/GuideDetail.vue'
import TrackForm from '@/components/track/TrackForm.vue'
import Layout from '@/layouts/Layout.vue'
import About from '@/pages/About.vue'
import CasesPage from '@/pages/CasesPage.vue'
import Dashboard from '@/pages/Dashboard.vue'
import EventsPage from '@/pages/EventsPage.vue'
import GuidesPage from '@/pages/GuidesPage.vue'
import Home from '@/pages/Home.vue'
import Login from '@/pages/Login.vue'
import NewsPage from '@/pages/NewsPage.vue'
import ModeratorCabinet from '@/pages/ModeratorCabinet.vue'
import AdminCabinet from '@/pages/AdminCabinet.vue'

import { createRouter, createWebHistory } from 'vue-router'
import { useAuthStore } from '@/stores/auth'


const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path:'/',
      component:Layout,
      children:[
        {path:'',component:Home},
        {path: 'about', component:About},
        {path: 'cases', component:CasesPage},
        {path: 'cases/:id', component:CaseDetail, name:"CaseDetail", props:true},
        {path: 'news', component:NewsPage},
        {path: 'events', component:EventsPage},
        {path: 'guides', component:GuidesPage},
        {path: 'guides/:id', component:GuideDetail, name:"GuideDetail", props:true},
        {path: 'upload', component:TrackForm},
        {path: 'login', component:Login},
        { 
          path: 'dashboard', 
          component: Dashboard,
          meta: { requiresAuth: true, roles: ['artist'] } 
        },
        { 
          path: 'moderator', 
          component: ModeratorCabinet,
          meta: { requiresAuth: true, roles: ['manager', 'admin'] } 
        },
        { 
          path: 'admin', 
          component: AdminCabinet,
          meta: { requiresAuth: true, roles: ['admin'] } 
        },
      ]
    }
  ],
})

router.beforeEach((to, from, next) => {
  const authStore = useAuthStore()
  
  // 1. Проверяем, нужна ли авторизация для страницы
  const requiresAuth = to.matched.some(record => record.meta.requiresAuth)
  const allowedRoles = to.meta.roles as string[] | undefined

  if (requiresAuth && !authStore.isAuthenticated) {
    next('/login')
  } 
  else if (requiresAuth && allowedRoles && !allowedRoles.includes(authStore.role || '')) {
    alert('ACCESS DENIED: Insufficient permissions')
    next('/dashboard') 
  } 
  else {
    next()
  }
})

export default router
