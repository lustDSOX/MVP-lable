import { ref, computed } from 'vue'
import { defineStore } from 'pinia'
import type { Permission } from '@/types/permissions'
import { usePermissionsStore } from '@/stores/permissions'

export type UserRole = 'artist' | 'moderator' | 'admin'

const STORAGE_KEY = 'mvp_lable_auth'

function loadSaved() {
  try {
    const raw = localStorage.getItem(STORAGE_KEY)
    if (!raw) return null
    return JSON.parse(raw) as {
      token: string
      artistName: string
      role: UserRole
      email: string
    }
  } catch {
    return null
  }
}

export const useAuthStore = defineStore('auth', () => {
  const saved = loadSaved()
  const token = ref<string | null>(saved?.token ?? null)
  const artistName = ref<string | null>(saved?.artistName ?? null)
  const role = ref<UserRole | null>(saved?.role ?? null)
  const email = ref<string | null>(saved?.email ?? null)
  const isLoading = ref(false)

  const isAuthenticated = computed(() => !!token.value)

  function persist() {
    if (!token.value) {
      localStorage.removeItem(STORAGE_KEY)
      return
    }
    localStorage.setItem(
      STORAGE_KEY,
      JSON.stringify({
        token: token.value,
        artistName: artistName.value,
        role: role.value,
        email: email.value,
      }),
    )
  }

  function setCredentials(
    newToken: string,
    name: string,
    newRole: UserRole,
    userEmail: string,
  ) {
    token.value = newToken
    artistName.value = name
    role.value = newRole
    email.value = userEmail
    persist()
  }

  function logout() {
    token.value = null
    artistName.value = null
    role.value = null
    email.value = null
    persist()
  }

  function can(permission: Permission): boolean {
    if (!isAuthenticated.value) return false
    if (role.value === 'admin') return true
    const perm = usePermissionsStore()
    perm.hydrate()
    return perm.permissionsFor(email.value || '', role.value).includes(permission)
  }

  function myPermissions(): Permission[] {
    if (role.value === 'admin') {
      return [
        'releases.moderate',
        'news.manage',
        'events.manage',
        'guides.manage',
        'users.manage',
        'permissions.manage',
      ]
    }
    const perm = usePermissionsStore()
    perm.hydrate()
    return perm.permissionsFor(email.value || '', role.value)
  }

  async function login(userEmail: string, password: string) {
    isLoading.value = true
    try {
      await new Promise((r) => setTimeout(r, 400))
      const e = userEmail.trim().toLowerCase()
      if (e === 'admin@label.ru' && password === 'admin123') {
        setCredentials('mock-jwt-admin', 'System Overlord', 'admin', e)
        return true
      }
      if (
        (e === 'moderator@label.ru' || e === 'manager@label.ru') &&
        (password === 'mod123' || password === 'manager123')
      ) {
        setCredentials('mock-jwt-mod', 'Chief Editor', 'moderator', e)
        return true
      }
      if (e === 'news@label.ru' && password === 'news123') {
        setCredentials('mock-jwt-news', 'News Desk', 'moderator', e)
        return true
      }
      if (e === 'events@label.ru' && password === 'events123') {
        setCredentials('mock-jwt-events', 'Events Desk', 'moderator', e)
        return true
      }
      if (e === 'staff@label.ru' && password === 'staff123') {
        setCredentials('mock-jwt-staff', 'Full Staff', 'moderator', e)
        return true
      }
      if (e === 'demo@label.ru' && password === 'demo123') {
        setCredentials('mock-jwt-artist', 'DJ Neon', 'artist', e)
        return true
      }
      if (password.length >= 6) {
        const name = e.split('@')[0] || 'Artist'
        setCredentials(`mock-jwt-${Date.now()}`, name, 'artist', e)
        return true
      }
      throw new Error('Неверные данные')
    } finally {
      isLoading.value = false
    }
  }

  async function register(userEmail: string, password: string, name: string) {
    isLoading.value = true
    try {
      await new Promise((r) => setTimeout(r, 500))
      if (password.length < 6) throw new Error('Пароль минимум 6 символов')
      if (!userEmail.includes('@')) throw new Error('Некорректный email')
      setCredentials(
        `mock-jwt-${Date.now()}`,
        name || userEmail.split('@')[0],
        'artist',
        userEmail.trim().toLowerCase(),
      )
      return true
    } finally {
      isLoading.value = false
    }
  }

  return {
    token,
    artistName,
    role,
    email,
    isAuthenticated,
    isLoading,
    login,
    register,
    logout,
    can,
    myPermissions,
  }
})
