import Layout from '@/layouts/Layout.vue'
import Home from '@/pages/Home.vue'
import { createRouter, createWebHistory } from 'vue-router'
import { useAuthStore } from '@/stores/auth'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      component: Layout,
      children: [
        { path: '', component: Home },
        { path: 'about', component: () => import('@/pages/About.vue') },
        { path: 'cases', component: () => import('@/pages/CasesPage.vue') },
        {
          path: 'cases/:id',
          name: 'CaseDetail',
          component: () => import('@/components/cases/CaseDetail.vue'),
          props: true,
        },
        { path: 'news', component: () => import('@/pages/NewsPage.vue') },
        { path: 'events', component: () => import('@/pages/EventsPage.vue') },
        { path: 'guides', component: () => import('@/pages/GuidesPage.vue') },
        {
          path: 'guides/:id',
          name: 'GuideDetail',
          component: () => import('@/components/guides/GuideDetail.vue'),
          props: true,
        },
        { path: 'upload', component: () => import('@/components/track/TrackForm.vue') },
        { path: 'login', component: () => import('@/pages/Login.vue') },
        { path: 'purchase', component: () => import('@/pages/PurchaseStub.vue') },
        {
          path: 'dashboard',
          component: () => import('@/pages/Dashboard.vue'),
          meta: { requiresAuth: true, roles: ['artist'] },
        },
        {
          path: 'moderator',
          component: () => import('@/pages/ModeratorCabinet.vue'),
          meta: { requiresAuth: true, roles: ['manager', 'admin'] },
        },
        {
          path: 'admin',
          component: () => import('@/pages/AdminCabinet.vue'),
          meta: { requiresAuth: true, roles: ['admin'] },
        },
      ],
    },
  ],
  scrollBehavior() {
    return { top: 0 }
  },
})

router.beforeEach((to, _from, next) => {
  const authStore = useAuthStore()
  const requiresAuth = to.matched.some((record) => record.meta.requiresAuth)
  const allowedRoles = to.meta.roles as string[] | undefined

  if (requiresAuth && !authStore.isAuthenticated) {
    next('/login')
  } else if (requiresAuth && allowedRoles && !allowedRoles.includes(authStore.role || '')) {
    next('/dashboard')
  } else {
    next()
  }
})

export default router
