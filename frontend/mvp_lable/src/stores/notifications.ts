import { defineStore } from 'pinia'

export type NotifType =
  | 'release_pending'
  | 'moderation_decision'
  | 'change_request'
  | 'admin_message'
  | 'system'
  | 'chat_mention'

export interface AppNotification {
  id: string
  userEmail: string
  title: string
  body: string
  type: NotifType
  read: boolean
  createdAt: string
  meta?: Record<string, string>
}

const KEY = 'mvp_notifications_v1'

function load(): AppNotification[] {
  try {
    const raw = localStorage.getItem(KEY)
    if (raw) return JSON.parse(raw)
  } catch { /* */ }
  return []
}

function save(list: AppNotification[]) {
  localStorage.setItem(KEY, JSON.stringify(list.slice(0, 500)))
}

export const useNotificationsStore = defineStore('notifications', {
  state: () => ({
    items: [] as AppNotification[],
    hydrated: false,
  }),
  getters: {
    forUser: (s) => (email: string) =>
      s.items
        .filter((n) => n.userEmail.toLowerCase() === email.toLowerCase())
        .sort((a, b) => b.createdAt.localeCompare(a.createdAt)),
    unreadCount: (s) => (email: string) =>
      s.items.filter((n) => n.userEmail.toLowerCase() === email.toLowerCase() && !n.read).length,
  },
  actions: {
    hydrate() {
      if (this.hydrated) return
      this.items = load()
      this.hydrated = true
    },
    persist() {
      save(this.items)
    },
    notify(payload: Omit<AppNotification, 'id' | 'read' | 'createdAt'> & { read?: boolean }) {
      this.hydrate()
      const n: AppNotification = {
        id: `n-${Date.now()}-${Math.random().toString(36).slice(2, 7)}`,
        read: payload.read ?? false,
        createdAt: new Date().toISOString(),
        userEmail: payload.userEmail,
        title: payload.title,
        body: payload.body,
        type: payload.type,
        meta: payload.meta,
      }
      this.items.unshift(n)
      this.persist()
      return n.id
    },
    notifyUser(email: string, title: string, body: string, type: NotifType = 'admin_message') {
      return this.notify({ userEmail: email, title, body, type })
    },
    notifyRoles(
      roles: string[],
      title: string,
      body: string,
      roleEmails: Record<string, string[]>,
    ) {
      const targets = new Set<string>()
      for (const r of roles) {
        for (const e of roleEmails[r] || []) targets.add(e.toLowerCase())
      }
      for (const email of targets) {
        this.notify({ userEmail: email, title, body, type: 'admin_message' })
      }
      return targets.size
    },
    markRead(id: string) {
      const n = this.items.find((x) => x.id === id)
      if (n) {
        n.read = true
        this.persist()
      }
    },
    markAllRead(email: string) {
      const e = email.toLowerCase()
      this.items.forEach((n) => {
        if (n.userEmail.toLowerCase() === e) n.read = true
      })
      this.persist()
    },
  },
})
