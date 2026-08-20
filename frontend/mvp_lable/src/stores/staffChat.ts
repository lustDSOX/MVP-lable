import { defineStore } from 'pinia'

export interface ChatUser {
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

const KEY = 'mvp_staff_dm_v3'
const PEERS_KEY = 'mvp_staff_dm_peers_v1'

export const ALL_CHAT_USERS: ChatUser[] = [
  { email: 'admin@label.ru', name: 'System Overlord' },
  { email: 'moderator@label.ru', name: 'Chief Editor' },
  { email: 'manager@label.ru', name: 'Manager' },
  { email: 'news@label.ru', name: 'News Desk' },
  { email: 'events@label.ru', name: 'Events Desk' },
  { email: 'staff@label.ru', name: 'Full Staff' },
  { email: 'demo@label.ru', name: 'DJ Neon' },
  { email: 'void@label.db', name: 'VoidStalker' },
  { email: 'alex.grid@mail.ru', name: 'Alex Grid' },
  { email: 'mira@bass.lab', name: 'Mira Bass' },
]

function loadMsgs(): DmMessage[] {
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
      body: 'Привет. Проверь очередь релизов.',
    },
  ]
}

function loadExtraPeers(): string[] {
  try {
    const raw = localStorage.getItem(PEERS_KEY)
    if (raw) return JSON.parse(raw)
  } catch { /* */ }
  return []
}

export const useStaffChatStore = defineStore('staffChat', {
  state: () => ({
    messages: [] as DmMessage[],
    extraPeers: [] as string[],
    hydrated: false,
  }),
  getters: {
    peersFor: (s) => (myEmail: string) => {
      const me = (myEmail || '').toLowerCase()
      const emails = new Set<string>()
      for (const e of s.extraPeers) emails.add(e)
      for (const m of s.messages) {
        if (m.fromEmail.toLowerCase() === me) emails.add(m.toEmail)
        if (m.toEmail.toLowerCase() === me) emails.add(m.fromEmail)
      }
      emails.delete(me)
      return [...emails]
        .map((email) => ALL_CHAT_USERS.find((u) => u.email.toLowerCase() === email.toLowerCase()) || { email, name: email })
        .sort((a, b) => a.name.localeCompare(b.name))
    },
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
      this.messages = loadMsgs()
      this.extraPeers = loadExtraPeers()
      this.hydrated = true
    },
    persist() {
      localStorage.setItem(KEY, JSON.stringify(this.messages.slice(-500)))
      localStorage.setItem(PEERS_KEY, JSON.stringify(this.extraPeers))
    },
    ensurePeer(email: string) {
      const e = email.toLowerCase()
      if (!this.extraPeers.some((x) => x.toLowerCase() === e)) {
        this.extraPeers.push(email)
        this.persist()
      }
    },
    send(fromEmail: string, toEmail: string, body: string) {
      this.hydrate()
      const text = body.trim()
      if (!text || !toEmail) return
      this.ensurePeer(toEmail)
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
