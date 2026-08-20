import { defineStore } from 'pinia'

export interface StaffPeer {
  email: string
  name: string
}

export interface DmMessage {
  id: string
  at: string
  fromEmail: string
  toEmail: string
  body: string
}

const KEY = 'mvp_staff_dm_v2'

export const STAFF_ROSTER: StaffPeer[] = [
  { email: 'admin@label.ru', name: 'System Overlord' },
  { email: 'moderator@label.ru', name: 'Chief Editor' },
  { email: 'manager@label.ru', name: 'Manager' },
  { email: 'news@label.ru', name: 'News Desk' },
  { email: 'events@label.ru', name: 'Events Desk' },
  { email: 'staff@label.ru', name: 'Full Staff' },
]

function load(): DmMessage[] {
  try {
    const raw = localStorage.getItem(KEY)
    if (raw) return JSON.parse(raw)
  } catch { /* */ }
  return [
    {
      id: 'seed-1',
      at: new Date(Date.now() - 7200000).toISOString(),
      fromEmail: 'admin@label.ru',
      toEmail: 'moderator@label.ru',
      body: 'Привет. Проверь очередь релизов на LIVE_REVISION.',
    },
    {
      id: 'seed-2',
      at: new Date(Date.now() - 3600000).toISOString(),
      fromEmail: 'moderator@label.ru',
      toEmail: 'admin@label.ru',
      body: 'Ок, смотрю Grid Runner EP.',
    },
  ]
}

export const useStaffChatStore = defineStore('staffChat', {
  state: () => ({
    messages: [] as DmMessage[],
    hydrated: false,
  }),
  getters: {
    peersFor: () => (myEmail: string) =>
      STAFF_ROSTER.filter((p) => p.email.toLowerCase() !== (myEmail || '').toLowerCase()),
    thread: (s) => (myEmail: string, peerEmail: string) => {
      const me = myEmail.toLowerCase()
      const peer = peerEmail.toLowerCase()
      return s.messages
        .filter(
          (m) =>
            (m.fromEmail.toLowerCase() === me && m.toEmail.toLowerCase() === peer) ||
            (m.fromEmail.toLowerCase() === peer && m.toEmail.toLowerCase() === me),
        )
        .sort((a, b) => a.at.localeCompare(b.at))
    },
  },
  actions: {
    hydrate() {
      if (this.hydrated) return
      this.messages = load()
      this.hydrated = true
    },
    persist() {
      localStorage.setItem(KEY, JSON.stringify(this.messages.slice(-500)))
    },
    send(fromEmail: string, toEmail: string, body: string) {
      this.hydrate()
      const text = body.trim()
      if (!text || !toEmail) return
      this.messages.push({
        id: `dm-${Date.now()}`,
        at: new Date().toISOString(),
        fromEmail,
        toEmail,
        body: text,
      })
      this.persist()
    },
  },
})
