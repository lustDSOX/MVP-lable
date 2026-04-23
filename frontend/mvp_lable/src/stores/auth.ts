// src/stores/auth.ts
import { defineStore } from 'pinia'
import { ref, computed } from 'vue'

const TOKEN_KEY = 'jwt_token'
const ARTIST_NAME_KEY = 'artist_name'
const ROLE_KEY = 'user_role' // Добавляем ключ для роли

export type UserRole = 'artist' | 'manager' | 'admin'

export const useAuthStore = defineStore('auth', () => {
  const token = ref<string | null>(localStorage.getItem(TOKEN_KEY))
  const artistName = ref<string>(localStorage.getItem(ARTIST_NAME_KEY) || '')
  const role = ref<UserRole | null>(localStorage.getItem(ROLE_KEY) as UserRole)
  const isLoading = ref(false)

  const isAuthenticated = computed(() => !!token.value)

  function setCredentials(jwtToken: string, name: string, userRole: UserRole) {
    token.value = jwtToken
    artistName.value = name
    role.value = userRole
    localStorage.setItem(TOKEN_KEY, jwtToken)
    localStorage.setItem(ARTIST_NAME_KEY, name)
    localStorage.setItem(ROLE_KEY, userRole)
  }

  function logout() {
    token.value = null
    artistName.value = ''
    role.value = null
    localStorage.removeItem(TOKEN_KEY)
    localStorage.removeItem(ARTIST_NAME_KEY)
    localStorage.removeItem(ROLE_KEY)
  }

  async function login(email: string, password: string) {
    isLoading.value = true
    try {
      await new Promise(resolve => setTimeout(resolve, 1000))
      
      // Имитация разных ролей для тестов
      if (email === 'admin@label.ru' && password === 'admin123') {
        setCredentials('fake-jwt-admin', 'System Overlord', 'admin')
        return true
      } else if (email === 'manager@label.ru' && password === 'manager123') {
        setCredentials('fake-jwt-manager', 'Chief Editor', 'manager')
        return true
      } else if (email === 'demo@label.ru' && password === 'demo123') {
        setCredentials('fake-jwt-artist', 'DJ Neon', 'artist')
        return true
      } else {
        throw new Error('Неверные данные')
      }
    } finally {
      isLoading.value = false
    }
  }

  return { token, artistName, role, isAuthenticated, isLoading, login, logout }
})