import { defineStore } from 'pinia'

export interface ChatMessage {
  id: string
  at: string
  fromEmail: string
  fromName: string
  body: string
}

const KEY = 'mvp_staff_chat_v1'

function load(): ChatMessage[] {
  try {
    const raw = localStorage.getItem(KEY)
    if (raw) return JSON.parse(raw)
  } catch { /* */ }
  return [
    {
      id: 'seed-1',
      at: new Date(Date.now() - 3600000).toISOString(),
      fromEmail: 'admin@label.ru',
      fromName: 'System Overlord',
      body: 'Внутренний канал staff/admin. Сообщения видны только персоналу.',
    },
  ]
}

export const useStaffChatStore = defineStore('staffChat', {
  state: () => ({
    messages: [] as ChatMessage[],
    hydrated: false,
  }),
  actions: {
    hydrate() {
      if (this.hydrated) return
      this.messages = load()
      this.hydrated = true
    },
    persist() {
      localStorage.setItem(KEY, JSON.stringify(this.messages.slice(-200)))
    },
    send(fromEmail: string, fromName: string, body: string) {
      this.hydrate()
      const text = body.trim()
      if (!text) return
      this.messages.push({
        id: `c-${Date.now()}`,
        at: new Date().toISOString(),
        fromEmail,
        fromName,
        body: text,
      })
      this.persist()
    },
  },
})
