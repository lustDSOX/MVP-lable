import Layout from '@/layouts/Layout.vue'
import Home from '@/pages/Home.vue'
import { createRouter, createWebHistory } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import type { Permission } from '@/types/permissions'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      component: Layout,
      children: [
        { path: '', component: Home, meta: { title: 'Home' } },
        { path: 'about', component: () => import('@/pages/About.vue'), meta: { title: 'About' } },
        { path: 'cases', component: () => import('@/pages/CasesPage.vue'), meta: { title: 'Cases' } },
        {
          path: 'cases/:id',
          name: 'CaseDetail',
          component: () => import('@/components/cases/CaseDetail.vue'),
          props: true,
        },
        { path: 'news', component: () => import('@/pages/NewsPage.vue'), meta: { title: 'News' } },
        { path: 'events', component: () => import('@/pages/EventsPage.vue'), meta: { title: 'Events' } },
        { path: 'guides', component: () => import('@/pages/GuidesPage.vue'), meta: { title: 'Guides' } },
        {
          path: 'guides/:id',
          name: 'GuideDetail',
          component: () => import('@/components/guides/GuideDetail.vue'),
          props: true,
        },
        { path: 'upload', component: () => import('@/components/track/TrackForm.vue') },
        { path: 'login', component: () => import('@/pages/Login.vue'), meta: { title: 'Login' } },
        { path: 'notifications', component: () => import('@/pages/NotificationsPage.vue'), meta: { title: 'Notifications' } },
        { path: 'purchase', component: () => import('@/pages/PurchaseStub.vue'), meta: { title: 'Purchase' } },
        {
          path: 'dashboard',
          component: () => import('@/pages/Dashboard.vue'),
          meta: { requiresAuth: true, roles: ['artist'], title: 'Artist Cabinet' },
        },
        {
          path: 'staff',
          component: () => import('@/pages/StaffHub.vue'),
          meta: { requiresAuth: true, roles: ['moderator', 'admin'], title: 'Staff Cabinet' },
        },
        { path: 'moderator', redirect: '/staff' },
        { path: 'admin', redirect: '/staff' },
        {
          path: 'cabinet',
          redirect: () => {
            const auth = useAuthStore()
            const r = auth.effectiveRole()
            if (r === 'admin' || r === 'moderator') return '/staff'
            if (auth.isAuthenticated) return '/dashboard'
            return '/login'
          },
        },
      ],
    },
  ],
  scrollBehavior() {
    return { top: 0 }
  },
})

function homeForRole(role: string | null): string {
  if (role === 'admin' || role === 'moderator') return '/staff'
  return '/dashboard'
}

router.beforeEach((to, _from, next) => {
  const authStore = useAuthStore()
  const requiresAuth = to.matched.some((record) => record.meta.requiresAuth)
  const allowedRoles = to.meta.roles as string[] | undefined
  const needPerm = to.meta.permission as Permission | undefined

  const role = authStore.effectiveRole() || authStore.role

  if (requiresAuth && !authStore.isAuthenticated) {
    next({ path: '/login', query: { redirect: to.fullPath } })
    return
  }
  if (requiresAuth && allowedRoles && !allowedRoles.includes(role || '')) {
    next(homeForRole(role))
    return
  }
  if (needPerm && !authStore.can(needPerm)) {
    next(homeForRole(role))
    return
  }
  next()
})

router.afterEach((to) => {
  const nearest = [...to.matched].reverse().find((r) => r.meta?.title)
  const page = nearest?.meta?.title ? String(nearest.meta.title) : null
  document.title = page ? `${page} · MVP LABLE` : 'MVP LABLE'
})

export default router
