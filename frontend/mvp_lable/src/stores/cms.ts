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
  ticketUrl: string
  price: string
  capacity: string
  ageLimit: string
}

export interface GuideItem {
  id: string
  title: string
  excerpt: string
  body: string
  category: string
  status: CmsStatus
  updatedAt: string
}

const NEWS_KEY = 'mvp_lable_cms_news'
const EVENTS_KEY = 'mvp_lable_cms_events'
const GUIDES_KEY = 'mvp_lable_cms_guides'
const CMS_VER = 'mvp_lable_cms_v'
const CMS_VER_VAL = '4'

function seedNews(): NewsItem[] {
  const now = new Date().toISOString()
  return [
    {
      id: 'n1',
      title: 'GRID_OPENING',
      excerpt: 'Лейбл открывает сезон',
      body: '## Сезон открыт\n\nЛейбл запускает **новый цикл** релизов.\n\n- CLASS TICKETS\n- Live events\n\n[Кабинет](/dashboard)',
      date: '2026-03-01',
      status: 'published',
      updatedAt: now,
    },
    {
      id: 'n2',
      title: 'NEON_DROP',
      excerpt: 'Новый релиз в сети',
      body: '### NEON_DROP\n\nСтриминг со **всех площадок**.\n\n`premiere 2026-04-12`',
      date: '2026-04-12',
      status: 'published',
      updatedAt: now,
    },
    {
      id: 'n3',
      title: 'CHAIN_PROTOCOL',
      excerpt: 'Обновление пайплайна релизов',
      body: '## Protocol v2\n\nНовый **flow** модерации.\n\n1. Upload\n2. Contract\n3. Approve\n\n`status: live`',
      date: '2026-05-01',
      status: 'published',
      updatedAt: now,
    },
    {
      id: 'n4',
      title: 'LIVE_ARCHIVE',
      excerpt: 'Архив выступлений',
      body: '### Archive\n\nЗаписи с **UNDERGROUND_NIGHT**.\n\n![cover](https://picsum.photos/seed/live/800/400)',
      date: '2026-05-20',
      status: 'published',
      updatedAt: now,
    },
    {
      id: 'n5',
      title: 'DRAFT_ONLY',
      excerpt: 'Черновик',
      body: 'Не публикуется',
      date: '2026-06-01',
      status: 'draft',
      updatedAt: now,
    },
  ]
}

function seedGuides(): GuideItem[] {
  const now = new Date().toISOString()
  return [
    {
      id: 'g1',
      title: 'RELEASE_PIPELINE',
      excerpt: 'Как сдать релиз без отказов',
      body: '# Release pipeline\n\n1. **Метаданные** — title, genre, date\n2. **Обложка** 3000×3000\n3. **Треки** + тексты\n4. **Договор** — один на релиз\n\n> Модератор видит весь пакет целиком.',
      category: 'releases',
      status: 'published',
      updatedAt: now,
    },
    {
      id: 'g2',
      title: 'CONTRACT_SIGN',
      excerpt: 'Подписание договора',
      body: '## Договор\n\nОдин контракт на **весь релиз** (не на трек).\n\n- Проверь ФИО\n- Подпиши в кабинете\n- PDF уходит в архив',
      category: 'legal',
      status: 'published',
      updatedAt: now,
    },
    {
      id: 'g3',
      title: 'PLATFORMS_CONNECT',
      excerpt: 'Spotify / Apple / VK',
      body: '### Площадки\n\nПодключи OAuth в кабинете.\n\nСтатистика подтянется после первой синхронизации.',
      category: 'platforms',
      status: 'published',
      updatedAt: now,
    },
    {
      id: 'g4',
      title: 'INTERNAL_DRAFT',
      excerpt: 'Внутренний',
      body: 'draft',
      category: 'internal',
      status: 'draft',
      updatedAt: now,
    },
  ]
}

function seedEvents(): EventItem[] {
  const now = new Date().toISOString()
  return [
    {
      id: 'e1',
      title: 'UNDERGROUND_NIGHT',
      venue: 'Club Void',
      city: 'Moscow',
      date: '15 AUG',
      time: '23:00',
      description: 'Live set · CLASS TICKETS night',
      status: 'published',
      updatedAt: now,
      ticketUrl: '/purchase',
      price: '1500 RUB',
      capacity: '400',
      ageLimit: '18+',
    },
    {
      id: 'e2',
      title: 'WAREHOUSE_RITUAL',
      venue: 'Warehouse 7',
      city: 'SPB',
      date: '22 AUG',
      time: '22:00',
      description: 'Label showcase + guest DJs',
      status: 'published',
      updatedAt: now,
      ticketUrl: '/purchase',
      price: '2000 RUB',
      capacity: '800',
      ageLimit: '18+',
    },
    {
      id: 'e3',
      title: 'NEON_OPEN_AIR',
      venue: 'Roof Base',
      city: 'Moscow',
      date: '05 SEP',
      time: '20:00',
      description: 'Open-air set, limited capacity',
      status: 'published',
      updatedAt: now,
      ticketUrl: '/purchase',
      price: '2500 RUB',
      capacity: '300',
      ageLimit: '16+',
    },
    {
      id: 'e4',
      title: 'LABEL_SHOWCASE_DRAFT',
      venue: 'TBA',
      city: 'SPB',
      date: '12 SEP',
      time: '21:00',
      description: 'Draft event (not public)',
      status: 'draft',
      updatedAt: now,
      ticketUrl: '/purchase',
      price: 'TBA',
      capacity: 'TBA',
      ageLimit: '18+',
    },
  ]
}

export const useCmsStore = defineStore('cms', {
  state: () => ({
    news: [] as NewsItem[],
    events: [] as EventItem[],
    guides: [] as GuideItem[],
  }),
  getters: {
    publishedNews: (s) => s.news.filter((n) => n.status === 'published'),
    publishedEvents: (s) => s.events.filter((e) => e.status === 'published'),
    publishedGuides: (s) => s.guides.filter((g) => g.status === 'published'),
  },
  actions: {
    hydrate() {
      try {
        if (localStorage.getItem(CMS_VER) !== CMS_VER_VAL) {
          this.news = seedNews()
          this.events = seedEvents()
          this.guides = seedGuides()
          this.persist()
          localStorage.setItem(CMS_VER, CMS_VER_VAL)
          return
        }
        const n = localStorage.getItem(NEWS_KEY)
        const e = localStorage.getItem(EVENTS_KEY)
        const g = localStorage.getItem(GUIDES_KEY)
        this.news = n ? JSON.parse(n) : seedNews()
        this.events = e ? JSON.parse(e) : seedEvents()
        this.guides = g ? JSON.parse(g) : seedGuides()
      } catch {
        this.news = seedNews()
        this.events = seedEvents()
        this.guides = seedGuides()
      }
    },
    persist() {
      localStorage.setItem(NEWS_KEY, JSON.stringify(this.news))
      localStorage.setItem(EVENTS_KEY, JSON.stringify(this.events))
      localStorage.setItem(GUIDES_KEY, JSON.stringify(this.guides))
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
    upsertGuide(payload: Partial<GuideItem> & { title: string }) {
      const now = new Date().toISOString()
      if (payload.id) {
        const i = this.guides.findIndex((g) => g.id === payload.id)
        if (i >= 0) {
          this.guides[i] = { ...this.guides[i], ...payload, updatedAt: now } as GuideItem
          this.persist()
          return this.guides[i]
        }
      }
      const item: GuideItem = {
        id: 'g' + Date.now(),
        title: payload.title,
        excerpt: payload.excerpt || '',
        body: payload.body || '',
        category: payload.category || 'general',
        status: payload.status || 'draft',
        updatedAt: now,
      }
      this.guides.unshift(item)
      this.persist()
      return item
    },
    deleteGuide(id: string) {
      this.guides = this.guides.filter((g) => g.id !== id)
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
        ticketUrl: item.ticketUrl || '/purchase',
        price: item.price || '',
        capacity: item.capacity || '',
        ageLimit: item.ageLimit || '',
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
