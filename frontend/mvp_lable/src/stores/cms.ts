import { defineStore } from 'pinia'

export type CmsStatus = 'draft' | 'published'

export interface NewsItem {
  id: string
  title: string
  excerpt: string
  body: string
  date: string
  status: CmsStatus
  updatedAt: string
}

export interface EventItem {
  id: string
  title: string
  venue: string
  city: string
  date: string
  time: string
  description: string
  status: CmsStatus
  updatedAt: string
}

const NEWS_KEY = 'mvp_lable_cms_news'
const EVENTS_KEY = 'mvp_lable_cms_events'

function seedNews(): NewsItem[] {
  return [
    {
      id: 'n1',
      title: 'GRID_OPENING',
      excerpt: 'Лейбл открывает сезон',
      body: 'Полный текст анонса сезона.',
      date: '2026-03-01',
      status: 'published',
      updatedAt: new Date().toISOString(),
    },
    {
      id: 'n2',
      title: 'NEON_DROP',
      excerpt: 'Новый релиз в сети',
      body: 'Details of the drop.',
      date: '2026-04-12',
      status: 'published',
      updatedAt: new Date().toISOString(),
    },
  ]
}

function seedEvents(): EventItem[] {
  return [
    {
      id: 'e1',
      title: 'UNDERGROUND_NIGHT',
      venue: 'Club Void',
      city: 'Moscow',
      date: '15 AUG',
      time: '23:00',
      description: 'Live set night',
      status: 'published',
      updatedAt: new Date().toISOString(),
    },
    {
      id: 'e2',
      title: 'LABEL_SHOWCASE',
      venue: 'Warehouse 7',
      city: 'SPB',
      date: '02 SEP',
      time: '21:00',
      description: 'Artists of the label',
      status: 'draft',
      updatedAt: new Date().toISOString(),
    },
  ]
}

export const useCmsStore = defineStore('cms', {
  state: () => ({
    news: seedNews() as NewsItem[],
    events: seedEvents() as EventItem[],
  }),
  getters: {
    publishedNews: (s) => s.news.filter((n) => n.status === 'published'),
    publishedEvents: (s) => s.events.filter((e) => e.status === 'published'),
  },
  actions: {
    hydrate() {
      try {
        const n = localStorage.getItem(NEWS_KEY)
        const e = localStorage.getItem(EVENTS_KEY)
        if (n) this.news = JSON.parse(n)
        if (e) this.events = JSON.parse(e)
      } catch {
        /* seed */
      }
    },
    persist() {
      localStorage.setItem(NEWS_KEY, JSON.stringify(this.news))
      localStorage.setItem(EVENTS_KEY, JSON.stringify(this.events))
    },
    upsertNews(item: Omit<NewsItem, 'id' | 'updatedAt'> & { id?: string }) {
      const now = new Date().toISOString()
      if (item.id) {
        const i = this.news.findIndex((x) => x.id === item.id)
        if (i >= 0) {
          this.news[i] = { ...this.news[i], ...item, id: item.id, updatedAt: now }
          this.persist()
          return item.id
        }
      }
      const id = `n-${Date.now()}`
      this.news.unshift({
        id,
        title: item.title,
        excerpt: item.excerpt,
        body: item.body,
        date: item.date,
        status: item.status,
        updatedAt: now,
      })
      this.persist()
      return id
    },
    deleteNews(id: string) {
      this.news = this.news.filter((n) => n.id !== id)
      this.persist()
    },
    upsertEvent(item: Omit<EventItem, 'id' | 'updatedAt'> & { id?: string }) {
      const now = new Date().toISOString()
      if (item.id) {
        const i = this.events.findIndex((x) => x.id === item.id)
        if (i >= 0) {
          this.events[i] = { ...this.events[i], ...item, id: item.id, updatedAt: now }
          this.persist()
          return item.id
        }
      }
      const id = `e-${Date.now()}`
      this.events.unshift({
        id,
        title: item.title,
        venue: item.venue,
        city: item.city,
        date: item.date,
        time: item.time,
        description: item.description,
        status: item.status,
        updatedAt: now,
      })
      this.persist()
      return id
    },
    deleteEvent(id: string) {
      this.events = this.events.filter((e) => e.id !== id)
      this.persist()
    },
  },
})
