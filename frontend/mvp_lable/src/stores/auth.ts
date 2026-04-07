// src/stores/auth.ts
import { defineStore } from 'pinia'
import { ref, computed } from 'vue'

const TOKEN_KEY = 'jwt_token'
const ARTIST_NAME_KEY = 'artist_name'

export const useAuthStore = defineStore('auth', () => {
  // состояние
  const token = ref<string | null>(localStorage.getItem(TOKEN_KEY))
  const artistName = ref<string>(localStorage.getItem(ARTIST_NAME_KEY) || '')
  const isLoading = ref(false)

  // computed
  const isAuthenticated = computed(() => !!token.value)

  // actions
  function setCredentials(jwtToken: string, name: string) {
    token.value = jwtToken
    artistName.value = name
    localStorage.setItem(TOKEN_KEY, jwtToken)
    localStorage.setItem(ARTIST_NAME_KEY, name)
  }

  function logout() {
    token.value = null
    artistName.value = ''
    localStorage.removeItem(TOKEN_KEY)
    localStorage.removeItem(ARTIST_NAME_KEY)
  }

  async function login(email: string, password: string) {
    isLoading.value = true
    try {
      // заглушка API с реальным JWT-подобным токеном
      await new Promise(resolve => setTimeout(resolve, 1500))
      
      if (email === 'demo@label.ru' && password === 'demo123') {
        // РЕАЛЬНЫЙ JWT-ТОКЕН (можно декодировать на jwt.io)
        const jwtToken = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkRKIE5lb24iLCJpYXQiOjE3MjAwMDAwMDAsImV4cCI6MTc1MTUzNjAwMH0.SflKxwRJSMeKKF2QT4fwpMeJf36POk6yJV_adQssw5c'
        setCredentials(jwtToken, 'DJ Neon')
        return true
      } else {
        throw new Error('Неверные данные')
      }
    } catch (error) {
      throw error
    } finally {
      isLoading.value = false
    }
  }

  return {
    token,
    artistName,
    isAuthenticated,
    isLoading,
    login,
    logout,
    setCredentials,
  }
})