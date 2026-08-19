import { defineStore } from 'pinia'

export type AccountStatus = 'active' | 'blocked' | 'pending'

export interface Account {
  id: string
  name: string
  email: string
  role: 'artist' | 'moderator' | 'admin'
  status: AccountStatus
  registeredAt: string
}

export interface RegistrationRequest {
  id: string
  name: string
  email: string
  artistName: string
  createdAt: string
  note?: string
}

const USERS_KEY = 'mvp_lable_admin_users'
const REQS_KEY = 'mvp_lable_admin_reqs'

function seedUsers(): Account[] {
  return [
    {
      id: 'a1',
      name: 'DJ Neon',
      email: 'demo@label.ru',
      role: 'artist',
      status: 'active',
      registeredAt: '2026-01-10',
    },
    {
      id: 'a2',
      name: 'Chief Editor',
      email: 'moderator@label.ru',
      role: 'moderator',
      status: 'active',
      registeredAt: '2025-11-01',
    },
    {
      id: 'a3',
      name: 'SynthRider',
      email: 'synth@label.db',
      role: 'artist',
      status: 'active',
      registeredAt: '2025-10-15',
    },
    {
      id: 'a4',
      name: 'VoidStalker',
      email: 'void@label.db',
      role: 'artist',
      status: 'blocked',
      registeredAt: '2026-01-05',
    },
  ]
}

function seedReqs(): RegistrationRequest[] {
  return [
    {
      id: 'r1',
      name: 'Alex Grid',
      email: 'alex.grid@mail.ru',
      artistName: 'GridKid',
      createdAt: '2026-03-18',
      note: 'Хочет релиз EP',
    },
    {
      id: 'r2',
      name: 'Mira Bass',
      email: 'mira@bass.lab',
      artistName: 'MIRA',
      createdAt: '2026-03-19',
    },
  ]
}

export const useAdminStore = defineStore('admin', {
  state: () => ({
    users: seedUsers() as Account[],
    requests: seedReqs() as RegistrationRequest[],
    isLoading: false,
    error: null as string | null,
  }),
  getters: {
    totalUsers: (s) => s.users.length,
    blockedUsersCount: (s) => s.users.filter((u) => u.status === 'blocked').length,
    pendingRequests: (s) => s.requests,
  },
  actions: {
    hydrate() {
      try {
        const u = localStorage.getItem(USERS_KEY)
        const r = localStorage.getItem(REQS_KEY)
        if (u) this.users = JSON.parse(u)
        if (r) this.requests = JSON.parse(r)
      } catch {
        /* seed */
      }
    },
    persist() {
      localStorage.setItem(USERS_KEY, JSON.stringify(this.users))
      localStorage.setItem(REQS_KEY, JSON.stringify(this.requests))
    },
    async fetchUsers() {
      this.isLoading = true
      this.hydrate()
      await new Promise((r) => setTimeout(r, 200))
      this.isLoading = false
    },
    upsertUser(partial: Partial<Account> & { email: string; name: string }) {
      if (partial.id) {
        const i = this.users.findIndex((u) => u.id === partial.id)
        if (i >= 0) {
          this.users[i] = { ...this.users[i], ...partial } as Account
          this.persist()
          return partial.id
        }
      }
      const id = `a-${Date.now()}`
      this.users.push({
        id,
        name: partial.name,
        email: partial.email.toLowerCase(),
        role: partial.role || 'artist',
        status: partial.status || 'active',
        registeredAt: new Date().toISOString().slice(0, 10),
      })
      this.persist()
      return id
    },
    blockUser(id: string) {
      const u = this.users.find((x) => x.id === id)
      if (u) {
        u.status = 'blocked'
        this.persist()
      }
    },
    unblockUser(id: string) {
      const u = this.users.find((x) => x.id === id)
      if (u) {
        u.status = 'active'
        this.persist()
      }
    },
    deleteUser(id: string) {
      this.users = this.users.filter((u) => u.id !== id)
      this.persist()
    },
    approveRequest(reqId: string) {
      const req = this.requests.find((r) => r.id === reqId)
      if (!req) return
      this.upsertUser({
        name: req.artistName || req.name,
        email: req.email,
        role: 'artist',
        status: 'active',
      })
      this.requests = this.requests.filter((r) => r.id !== reqId)
      this.persist()
    },
    rejectRequest(reqId: string) {
      this.requests = this.requests.filter((r) => r.id !== reqId)
      this.persist()
    },
  },
})
