import { defineStore } from 'pinia'

export type PlatformId = 'spotify' | 'apple' | 'yandex' | 'vk'

export interface PlatformAccount {
  id: PlatformId
  label: string
  connected: boolean
  accountName: string | null
  connectedAt: string | null
}

const STORAGE = 'mvp_lable_platforms_v2'

function defaults(): PlatformAccount[] {
  const at = new Date().toISOString()
  return [
    { id: 'spotify', label: 'Spotify', connected: true, accountName: 'mock_spotify_user', connectedAt: at },
    { id: 'apple', label: 'Apple Music', connected: true, accountName: 'mock_apple_user', connectedAt: at },
    { id: 'yandex', label: 'Яндекс Музыка', connected: true, accountName: 'mock_yandex_user', connectedAt: at },
    { id: 'vk', label: 'VK Music', connected: true, accountName: 'mock_vk_user', connectedAt: at },
  ]
}

export const usePlatformsStore = defineStore('platforms', {
  state: () => ({
    accounts: defaults() as PlatformAccount[],
    busyId: null as PlatformId | null,
  }),

  getters: {
    connectedCount: (s) => s.accounts.filter((a) => a.connected).length,
  },

  actions: {
    hydrate() {
      try {
        const raw = localStorage.getItem(STORAGE)
        if (raw) this.accounts = JSON.parse(raw)
      } catch {
        /* keep defaults */
      }
    },
    persist() {
      localStorage.setItem(STORAGE, JSON.stringify(this.accounts))
    },
    async connect(id: PlatformId) {
      this.busyId = id
      await new Promise((r) => setTimeout(r, 700))
      const row = this.accounts.find((a) => a.id === id)
      if (row) {
        row.connected = true
        row.accountName = `mock_${id}_user`
        row.connectedAt = new Date().toISOString()
      }
      this.persist()
      this.busyId = null
    },
    async disconnect(id: PlatformId) {
      this.busyId = id
      await new Promise((r) => setTimeout(r, 400))
      const row = this.accounts.find((a) => a.id === id)
      if (row) {
        row.connected = false
        row.accountName = null
        row.connectedAt = null
      }
      this.persist()
      this.busyId = null
    },
  },
})
