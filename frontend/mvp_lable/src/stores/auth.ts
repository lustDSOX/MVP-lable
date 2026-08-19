import { ref, computed } from 'vue'
import { defineStore } from 'pinia'
import type { Permission } from '@/types/permissions'
import { usePermissionsStore } from '@/stores/permissions'

export type UserRole = 'artist' | 'moderator' | 'admin'

const STORAGE_KEY = 'mvp_lable_auth'

const DEMO_ACCOUNTS: Record<
  string,
  { password: string; role: UserRole; name: string }
> = {
  'admin@label.ru': { password: 'admin123', role: 'admin', name: 'System Overlord' },
  'moderator@label.ru': { password: 'mod123', role: 'moderator', name: 'Chief Editor' },
  'manager@label.ru': { password: 'mod123', role: 'moderator', name: 'Chief Editor' },
  'news@label.ru': { password: 'news123', role: 'moderator', name: 'News Desk' },
  'events@label.ru': { password: 'events123', role: 'moderator', name: 'Events Desk' },
  'staff@label.ru': { password: 'staff123', role: 'moderator', name: 'Full Staff' },
  'demo@label.ru': { password: 'demo123', role: 'artist', name: 'DJ Neon' },
}

function loadSaved() {
  try {
    const raw = localStorage.getItem(STORAGE_KEY)
    if (!raw) return null
    const data = JSON.parse(raw) as {
      token: string
      artistName: string
      role: UserRole
      email: string
    }
    if (!data.token) return null
    const email = (data.email || '').toLowerCase()
    if (DEMO_ACCOUNTS[email] && data.role !== DEMO_ACCOUNTS[email].role) {
      data.role = DEMO_ACCOUNTS[email].role
    }
    return data
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
    email.value = userEmail.toLowerCase()
    persist()
  }

  function logout() {
    token.value = null
    artistName.value = null
    role.value = null
    email.value = null
    persist()
  }

  function effectiveRole(): UserRole | null {
    const e = (email.value || '').toLowerCase()
    if (e && DEMO_ACCOUNTS[e]) return DEMO_ACCOUNTS[e].role
    return role.value
  }

  function effectiveRoles(): string[] {
    const e = (email.value || '').toLowerCase()
    if (e === 'staff@label.ru') return ['moderator', 'news_editor', 'events_editor']
    if (e === 'news@label.ru') return ['news_editor']
    if (e === 'events@label.ru') return ['events_editor']
    if (e === 'admin@label.ru') return ['admin']
    if (e === 'moderator@label.ru' || e === 'manager@label.ru') return ['moderator']
    const r = effectiveRole()
    return r ? [r] : []
  }

  function can(permission: Permission): boolean {
    if (!isAuthenticated.value) return false
    const roles = effectiveRoles()
    if (roles.includes('admin')) return true
    const perm = usePermissionsStore()
    perm.hydrate()
    return perm.permissionsForRoles(roles).includes(permission)
  }

  function myPermissions(): Permission[] {
    const roles = effectiveRoles()
    const perm = usePermissionsStore()
    perm.hydrate()
    return perm.permissionsForRoles(roles)
  }

  async function login(userEmail: string, password: string): Promise<UserRole> {
    isLoading.value = true
    try {
      await new Promise((r) => setTimeout(r, 200))
      const e = userEmail.trim().toLowerCase()
      const pwd = password.trim()
      const demo = DEMO_ACCOUNTS[e]
      if (demo) {
        if (pwd !== demo.password) throw new Error(`Неверный пароль для ${e}`)
        setCredentials(`mock-jwt-${demo.role}`, demo.name, demo.role, e)
        return demo.role
      }
      if (pwd.length >= 6) {
        const name = e.split('@')[0] || 'Artist'
        setCredentials(`mock-jwt-artist-${Date.now()}`, name, 'artist', e)
        return 'artist'
      }
      throw new Error('Неверные данные')
    } finally {
      isLoading.value = false
    }
  }

  async function register(userEmail: string, password: string, name: string): Promise<UserRole> {
    isLoading.value = true
    try {
      await new Promise((r) => setTimeout(r, 300))
      if (password.length < 6) throw new Error('Пароль минимум 6 символов')
      if (!userEmail.includes('@')) throw new Error('Некорректный email')
      const e = userEmail.trim().toLowerCase()
      if (DEMO_ACCOUNTS[e]) throw new Error('Этот email зарезервирован. Войдите с demo-паролем.')
      setCredentials(`mock-jwt-${Date.now()}`, name || e.split('@')[0], 'artist', e)
      return 'artist'
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
    effectiveRole,
    effectiveRoles,
  }
})
