<template>
  <div class="min-h-screen pt-24 px-4 pb-12 text-white font-['Inter',sans-serif]">
    <div class="max-w-5xl mx-auto">
      <h1 class="font-mono text-2xl uppercase text-[#39FF14] mb-2">Staff_Hub // MOCK</h1>
      <p class="font-mono text-[10px] text-gray-500 uppercase mb-6">
        {{ auth.artistName }} · {{ auth.email }} · {{ auth.role }}
      </p>

      <div class="flex flex-wrap gap-2 mb-8 border border-[#333] p-1">
        <button
          v-for="tab in availableTabs"
          :key="tab.id"
          type="button"
          class="min-h-[44px] px-4 font-mono text-xs uppercase"
          :class="active === tab.id ? 'bg-[#39FF14] text-black' : 'text-gray-400'"
          @click="active = tab.id"
        >
          {{ tab.label }}
        </button>
      </div>

      <p v-if="!availableTabs.length" class="font-mono text-sm text-[#ff0000]">
        Нет выданных прав. Попроси admin выдать permission в матрице.
      </p>

      <div v-if="active === 'releases'" class="space-y-4">
        <p class="font-mono text-xs text-gray-400 uppercase">Очередь релизов</p>
        <router-link
          to="/moderator"
          class="inline-block border-2 border-[#39FF14] text-[#39FF14] font-mono text-sm uppercase px-4 py-3 min-h-[44px]"
        >
          Open release queue →
        </router-link>
      </div>

      <div v-else-if="active === 'news'" class="space-y-6">
        <form class="border-2 border-[#333] p-4 space-y-3" @submit.prevent="saveNews">
          <p class="font-mono text-xs text-[#39FF14] uppercase">{{ editingNewsId ? 'Edit' : 'New' }} news</p>
          <input v-model="newsForm.title" required placeholder="TITLE" class="field" />
          <input v-model="newsForm.excerpt" placeholder="EXCERPT" class="field" />
          <textarea v-model="newsForm.body" rows="3" placeholder="BODY" class="field" />
          <input v-model="newsForm.date" type="date" class="field" />
          <select v-model="newsForm.status" class="field">
            <option value="draft">draft</option>
            <option value="published">published</option>
          </select>
          <div class="flex gap-2 flex-wrap">
            <button type="submit" class="btn-green">Save</button>
            <button v-if="editingNewsId" type="button" class="btn-muted" @click="resetNews">Cancel</button>
          </div>
        </form>
        <article
          v-for="n in cms.news"
          :key="n.id"
          class="border border-[#333] p-4 flex flex-col sm:flex-row sm:items-center gap-3 justify-between"
        >
          <div>
            <p class="font-mono text-sm uppercase text-white">{{ n.title }}</p>
            <p class="font-mono text-[10px] text-gray-500">{{ n.status }} · {{ n.date }}</p>
          </div>
          <div class="flex gap-2">
            <button type="button" class="btn-muted" @click="editNews(n)">Edit</button>
            <button type="button" class="btn-red" @click="cms.deleteNews(n.id)">Del</button>
          </div>
        </article>
      </div>

      <div v-else-if="active === 'events'" class="space-y-6">
        <form class="border-2 border-[#333] p-4 space-y-3" @submit.prevent="saveEvent">
          <p class="font-mono text-xs text-[#39FF14] uppercase">{{ editingEventId ? 'Edit' : 'New' }} event</p>
          <input v-model="eventForm.title" required placeholder="TITLE" class="field" />
          <input v-model="eventForm.venue" placeholder="VENUE" class="field" />
          <input v-model="eventForm.city" placeholder="CITY" class="field" />
          <input v-model="eventForm.date" placeholder="15 AUG" class="field" />
          <input v-model="eventForm.time" placeholder="23:00" class="field" />
          <textarea v-model="eventForm.description" rows="2" placeholder="DESC" class="field" />
          <select v-model="eventForm.status" class="field">
            <option value="draft">draft</option>
            <option value="published">published</option>
          </select>
          <div class="flex gap-2 flex-wrap">
            <button type="submit" class="btn-green">Save</button>
            <button v-if="editingEventId" type="button" class="btn-muted" @click="resetEvent">Cancel</button>
          </div>
        </form>
        <article
          v-for="ev in cms.events"
          :key="ev.id"
          class="border border-[#333] p-4 flex flex-col sm:flex-row sm:items-center gap-3 justify-between"
        >
          <div>
            <p class="font-mono text-sm uppercase text-white">{{ ev.title }}</p>
            <p class="font-mono text-[10px] text-gray-500">
              {{ ev.status }} · {{ ev.city }} · {{ ev.date }} {{ ev.time }}
            </p>
          </div>
          <div class="flex gap-2">
            <button type="button" class="btn-muted" @click="editEvent(ev)">Edit</button>
            <button type="button" class="btn-red" @click="cms.deleteEvent(ev.id)">Del</button>
          </div>
        </article>
      </div>

      <div v-else-if="active === 'matrix'" class="overflow-x-auto">
        <p class="font-mono text-[10px] text-gray-500 uppercase mb-4">Матрица доступа · localStorage</p>
        <table class="w-full text-left border border-[#333] min-w-[640px]">
          <thead>
            <tr class="border-b border-[#333] font-mono text-[10px] uppercase text-gray-500">
              <th class="p-3">Staff</th>
              <th v-for="p in ALL_PERMISSIONS" :key="p.key" class="p-2 text-center">
                {{ p.label.split(' ')[0] }}
              </th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="u in perm.staff" :key="u.id" class="border-b border-[#222]">
              <td class="p-3 font-mono text-xs">
                <div class="text-white uppercase">{{ u.name }}</div>
                <div class="text-gray-500">{{ u.email }} · {{ u.role }}</div>
              </td>
              <td v-for="p in ALL_PERMISSIONS" :key="p.key" class="p-2 text-center">
                <input
                  type="checkbox"
                  class="w-5 h-5 accent-[#39FF14]"
                  :checked="u.permissions.includes(p.key)"
                  @change="perm.setPermission(u.id, p.key, ($event.target as HTMLInputElement).checked)"
                />
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted, reactive } from 'vue'
import { useAuthStore } from '@/stores/auth'
import { useCmsStore, type NewsItem, type EventItem } from '@/stores/cms'
import { usePermissionsStore } from '@/stores/permissions'
import { ALL_PERMISSIONS } from '@/types/permissions'

const auth = useAuthStore()
const cms = useCmsStore()
const perm = usePermissionsStore()

onMounted(() => {
  cms.hydrate()
  perm.hydrate()
  if (availableTabs.value.length) active.value = availableTabs.value[0].id
})

const availableTabs = computed(() => {
  const tabs: { id: string; label: string }[] = []
  if (auth.can('releases.moderate')) tabs.push({ id: 'releases', label: 'Releases' })
  if (auth.can('news.manage')) tabs.push({ id: 'news', label: 'News' })
  if (auth.can('events.manage')) tabs.push({ id: 'events', label: 'Events' })
  if (auth.can('permissions.manage')) tabs.push({ id: 'matrix', label: 'Access matrix' })
  return tabs
})

const active = ref('news')

const editingNewsId = ref<string | null>(null)
const newsForm = reactive({
  title: '',
  excerpt: '',
  body: '',
  date: new Date().toISOString().slice(0, 10),
  status: 'draft' as 'draft' | 'published',
})

function resetNews() {
  editingNewsId.value = null
  newsForm.title = ''
  newsForm.excerpt = ''
  newsForm.body = ''
  newsForm.date = new Date().toISOString().slice(0, 10)
  newsForm.status = 'draft'
}
function editNews(n: NewsItem) {
  editingNewsId.value = n.id
  newsForm.title = n.title
  newsForm.excerpt = n.excerpt
  newsForm.body = n.body
  newsForm.date = n.date
  newsForm.status = n.status
}
function saveNews() {
  cms.upsertNews({
    id: editingNewsId.value || undefined,
    title: newsForm.title,
    excerpt: newsForm.excerpt,
    body: newsForm.body,
    date: newsForm.date,
    status: newsForm.status,
  })
  resetNews()
}

const editingEventId = ref<string | null>(null)
const eventForm = reactive({
  title: '',
  venue: '',
  city: '',
  date: '',
  time: '',
  description: '',
  status: 'draft' as 'draft' | 'published',
})
function resetEvent() {
  editingEventId.value = null
  eventForm.title = ''
  eventForm.venue = ''
  eventForm.city = ''
  eventForm.date = ''
  eventForm.time = ''
  eventForm.description = ''
  eventForm.status = 'draft'
}
function editEvent(ev: EventItem) {
  editingEventId.value = ev.id
  eventForm.title = ev.title
  eventForm.venue = ev.venue
  eventForm.city = ev.city
  eventForm.date = ev.date
  eventForm.time = ev.time
  eventForm.description = ev.description
  eventForm.status = ev.status
}
function saveEvent() {
  cms.upsertEvent({
    id: editingEventId.value || undefined,
    title: eventForm.title,
    venue: eventForm.venue,
    city: eventForm.city,
    date: eventForm.date,
    time: eventForm.time,
    description: eventForm.description,
    status: eventForm.status,
  })
  resetEvent()
}
</script>

<style scoped>
.field {
  width: 100%;
  background: #000;
  border: 2px solid #333;
  color: #fff;
  font-family: 'JetBrains Mono', monospace;
  font-size: 0.85rem;
  padding: 0.75rem;
  text-transform: uppercase;
  min-height: 44px;
}
.btn-green {
  background: #39ff14;
  color: #000;
  font-family: 'JetBrains Mono', monospace;
  font-size: 0.75rem;
  text-transform: uppercase;
  padding: 0.75rem 1rem;
  min-height: 44px;
  border: none;
}
.btn-muted {
  background: #222;
  color: #9ca3af;
  font-family: 'JetBrains Mono', monospace;
  font-size: 0.7rem;
  text-transform: uppercase;
  padding: 0.75rem 1rem;
  min-height: 44px;
  border: none;
}
.btn-red {
  background: #ff0000;
  color: #000;
  font-family: 'JetBrains Mono', monospace;
  font-size: 0.7rem;
  text-transform: uppercase;
  padding: 0.75rem 1rem;
  min-height: 44px;
  border: none;
}
</style>
