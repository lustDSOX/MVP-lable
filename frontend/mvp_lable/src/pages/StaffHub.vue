<template>
  <div class="min-h-screen pt-24 px-4 pb-16 text-white font-['Inter',sans-serif]">
    <div class="max-w-5xl mx-auto">
      <header class="border-b-4 border-[#39FF14] pb-4 mb-8">
        <p class="font-mono text-[10px] text-gray-500 uppercase tracking-widest mb-1">Staff_Cabinet // role-based</p>
        <h1 class="text-3xl sm:text-4xl font-black uppercase italic tracking-tight">{{ auth.artistName || 'STAFF' }}</h1>
        <div class="mt-3 flex flex-wrap gap-2 items-center">
          <span class="font-mono text-xs px-2 py-1 bg-[#39FF14] text-black font-bold uppercase">{{ auth.role }}</span>
          <span class="font-mono text-[10px] text-gray-500">{{ auth.email }}</span>
          <span v-for="p in myPerms" :key="p" class="font-mono text-[9px] border border-[#333] text-gray-400 px-2 py-0.5 uppercase">{{ p }}</span>
        </div>
      </header>

      <div v-if="availableTabs.length" class="flex flex-wrap gap-2 mb-8">
        <button v-for="tab in availableTabs" :key="tab.id" type="button" class="min-h-[44px] px-4 font-mono text-xs uppercase border-2" :class="active === tab.id ? 'bg-[#39FF14] text-black border-black' : 'border-[#333] text-gray-400'" @click="active = tab.id">{{ tab.label }}</button>
      </div>
      <p v-else class="font-mono text-sm text-[#ff0000] mb-8">Нет выданных прав. Admin → MATRIX.</p>

      <section v-if="active === 'releases'" class="space-y-4">
        <div class="flex flex-wrap gap-2 items-center justify-between">
          <p class="font-mono text-xs text-gray-400 uppercase">Очередь модерации релизов</p>
          <div class="flex gap-2">
            <button type="button" class="chip" :class="{ on: queueFilter === 'pending' }" @click="queueFilter = 'pending'">Pending</button>
            <button type="button" class="chip" :class="{ on: queueFilter === 'all' }" @click="queueFilter = 'all'">All</button>
          </div>
        </div>
        <article v-for="t in queueTracks" :key="t.id" class="border-2 border-[#333] bg-[#0a0a0a] p-4 flex flex-col sm:flex-row sm:items-center gap-4 justify-between">
          <div>
            <h3 class="font-black uppercase text-lg">{{ t.title }}</h3>
            <p class="font-mono text-[10px] text-gray-500 uppercase mt-1">{{ t.status }} · plays {{ t.plays ?? 0 }}<span v-if="t.rejectReason" class="text-[#ff0000]"> · {{ t.rejectReason }}</span></p>
          </div>
          <div class="flex flex-wrap gap-2">
            <button v-if="t.status === 'pending' || t.status === 'draft'" type="button" class="btn-green" @click="tracks.setStatus(t.id, 'published')">Approve</button>
            <button v-if="t.status !== 'rejected'" type="button" class="btn-red" @click="reject(t.id)">Reject</button>
            <button v-if="t.status === 'rejected'" type="button" class="btn-muted" @click="tracks.setStatus(t.id, 'pending')">Re-queue</button>
          </div>
        </article>
        <p v-if="!queueTracks.length" class="font-mono text-gray-600 text-sm">Очередь пуста</p>
      </section>

      <section v-else-if="active === 'news'" class="space-y-6">
        <form class="border-2 border-[#333] p-4 space-y-3" @submit.prevent="saveNews">
          <p class="font-mono text-xs text-[#39FF14] uppercase">{{ editingNewsId ? 'Edit' : 'New' }} news</p>
          <input v-model="newsForm.title" required placeholder="TITLE" class="field" />
          <input v-model="newsForm.excerpt" placeholder="EXCERPT" class="field" />
          <textarea v-model="newsForm.body" rows="3" placeholder="BODY" class="field" />
          <input v-model="newsForm.date" type="date" class="field" />
          <select v-model="newsForm.status" class="field"><option value="draft">draft</option><option value="published">published</option></select>
          <div class="flex gap-2 flex-wrap"><button type="submit" class="btn-green">Save</button><button v-if="editingNewsId" type="button" class="btn-muted" @click="resetNews">Cancel</button></div>
        </form>
        <article v-for="n in cms.news" :key="n.id" class="border border-[#333] p-4 flex flex-col sm:flex-row sm:items-center gap-3 justify-between">
          <div><p class="font-mono text-sm uppercase text-white">{{ n.title }}</p><p class="font-mono text-[10px] text-gray-500">{{ n.status }} · {{ n.date }}</p></div>
          <div class="flex gap-2"><button type="button" class="btn-muted" @click="editNews(n)">Edit</button><button type="button" class="btn-red" @click="cms.deleteNews(n.id)">Del</button></div>
        </article>
      </section>

      <section v-else-if="active === 'events'" class="space-y-6">
        <form class="border-2 border-[#333] p-4 space-y-3" @submit.prevent="saveEvent">
          <p class="font-mono text-xs text-[#39FF14] uppercase">{{ editingEventId ? 'Edit' : 'New' }} event</p>
          <input v-model="eventForm.title" required placeholder="TITLE" class="field" />
          <input v-model="eventForm.venue" placeholder="VENUE" class="field" />
          <input v-model="eventForm.city" placeholder="CITY" class="field" />
          <input v-model="eventForm.date" placeholder="15 AUG" class="field" />
          <input v-model="eventForm.time" placeholder="23:00" class="field" />
          <textarea v-model="eventForm.description" rows="2" placeholder="DESC" class="field" />
          <select v-model="eventForm.status" class="field"><option value="draft">draft</option><option value="published">published</option></select>
          <div class="flex gap-2 flex-wrap"><button type="submit" class="btn-green">Save</button><button v-if="editingEventId" type="button" class="btn-muted" @click="resetEvent">Cancel</button></div>
        </form>
        <article v-for="ev in cms.events" :key="ev.id" class="border border-[#333] p-4 flex flex-col sm:flex-row sm:items-center gap-3 justify-between">
          <div><p class="font-mono text-sm uppercase text-white">{{ ev.title }}</p><p class="font-mono text-[10px] text-gray-500">{{ ev.status }} · {{ ev.city }} · {{ ev.date }} {{ ev.time }}</p></div>
          <div class="flex gap-2"><button type="button" class="btn-muted" @click="editEvent(ev)">Edit</button><button type="button" class="btn-red" @click="cms.deleteEvent(ev.id)">Del</button></div>
        </article>
      </section>

      <section v-else-if="active === 'matrix'" class="space-y-4 overflow-x-auto">
        <p class="font-mono text-xs text-gray-400 uppercase mb-2">Матрица доступа staff</p>
        <table class="w-full text-left border border-[#333] min-w-[640px]">
          <thead><tr class="border-b border-[#333] font-mono text-[10px] text-gray-500 uppercase"><th class="p-3">User</th><th v-for="p in ALL_PERMISSIONS" :key="p.key" class="p-2 text-center">{{ p.label.split(' ')[0] }}</th></tr></thead>
          <tbody>
            <tr v-for="u in perm.staff" :key="u.id" class="border-b border-[#222]">
              <td class="p-3"><p class="font-mono text-xs text-white">{{ u.email }}</p><p class="font-mono text-[9px] text-gray-500">{{ u.role }} · {{ u.name }}</p></td>
              <td v-for="p in ALL_PERMISSIONS" :key="p.key" class="p-2 text-center">
                <input type="checkbox" class="w-5 h-5 accent-[#39FF14]" :checked="u.permissions.includes(p.key)" @change="perm.setPermission(u.id, p.key, ($event.target as HTMLInputElement).checked)" />
              </td>
            </tr>
          </tbody>
        </table>
      </section>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed, onMounted, reactive, ref, watch } from 'vue'
import { useAuthStore } from '@/stores/auth'
import { useCmsStore } from '@/stores/cms'
import { usePermissionsStore } from '@/stores/permissions'
import { useTracksStore } from '@/stores/tracks'
import { ALL_PERMISSIONS } from '@/types/permissions'
import type { NewsItem, EventItem } from '@/stores/cms'

const auth = useAuthStore()
const cms = useCmsStore()
const perm = usePermissionsStore()
const tracks = useTracksStore()
const myPerms = computed(() => auth.myPermissions())

const active = ref('releases')
const queueFilter = ref<'pending' | 'all'>('pending')

const availableTabs = computed(() => {
  const tabs: { id: string; label: string }[] = []
  if (auth.can('releases.moderate')) tabs.push({ id: 'releases', label: 'Релизы' })
  if (auth.can('news.manage')) tabs.push({ id: 'news', label: 'Новости' })
  if (auth.can('events.manage')) tabs.push({ id: 'events', label: 'События' })
  if (auth.can('permissions.manage')) tabs.push({ id: 'matrix', label: 'Matrix' })
  return tabs
})

watch(availableTabs, (tabs) => {
  if (!tabs.find((t) => t.id === active.value)) active.value = tabs[0]?.id || ''
}, { immediate: true })

const queueTracks = computed(() => {
  const list = tracks.tracks
  if (queueFilter.value === 'pending') return list.filter((t) => t.status === 'pending' || t.status === 'draft')
  return list
})

function reject(id: string) {
  const reason = window.prompt('Причина отказа', 'Не соответствует гайду')
  if (reason !== null) tracks.setStatus(id, 'rejected', reason || 'Rejected')
}

const editingNewsId = ref<string | null>(null)
const newsForm = reactive({ title: '', excerpt: '', body: '', date: new Date().toISOString().slice(0, 10), status: 'draft' as 'draft' | 'published' })
function resetNews() { editingNewsId.value = null; newsForm.title = ''; newsForm.excerpt = ''; newsForm.body = ''; newsForm.date = new Date().toISOString().slice(0, 10); newsForm.status = 'draft' }
function editNews(n: NewsItem) { editingNewsId.value = n.id; newsForm.title = n.title; newsForm.excerpt = n.excerpt; newsForm.body = n.body; newsForm.date = n.date; newsForm.status = n.status }
function saveNews() { cms.upsertNews({ id: editingNewsId.value || undefined, title: newsForm.title, excerpt: newsForm.excerpt, body: newsForm.body, date: newsForm.date, status: newsForm.status }); resetNews() }

const editingEventId = ref<string | null>(null)
const eventForm = reactive({ title: '', venue: '', city: '', date: '15 AUG', time: '23:00', description: '', status: 'draft' as 'draft' | 'published' })
function resetEvent() { editingEventId.value = null; eventForm.title = ''; eventForm.venue = ''; eventForm.city = ''; eventForm.date = '15 AUG'; eventForm.time = '23:00'; eventForm.description = ''; eventForm.status = 'draft' }
function editEvent(ev: EventItem) { editingEventId.value = ev.id; eventForm.title = ev.title; eventForm.venue = ev.venue; eventForm.city = ev.city; eventForm.date = ev.date; eventForm.time = ev.time; eventForm.description = ev.description; eventForm.status = ev.status }
function saveEvent() { cms.upsertEvent({ id: editingEventId.value || undefined, title: eventForm.title, venue: eventForm.venue, city: eventForm.city, date: eventForm.date, time: eventForm.time, description: eventForm.description, status: eventForm.status }); resetEvent() }

onMounted(() => { cms.hydrate(); perm.hydrate(); tracks.fetchTracks() })
</script>

<style scoped>
.field { display: block; width: 100%; background: #000; border: 2px solid #333; color: #fff; padding: 0.75rem; font-family: 'JetBrains Mono', monospace; font-size: 0.875rem; }
.btn-green { background: #39ff14; color: #000; font-family: 'JetBrains Mono', monospace; font-size: 0.75rem; text-transform: uppercase; padding: 0.5rem 1rem; min-height: 44px; border: 2px solid #000; font-weight: 700; }
.btn-red { background: #ff0000; color: #fff; font-family: 'JetBrains Mono', monospace; font-size: 0.75rem; text-transform: uppercase; padding: 0.5rem 1rem; min-height: 44px; border: 2px solid #000; }
.btn-muted { background: #222; color: #ccc; font-family: 'JetBrains Mono', monospace; font-size: 0.75rem; text-transform: uppercase; padding: 0.5rem 1rem; min-height: 44px; border: 2px solid #444; }
.chip { font-family: 'JetBrains Mono', monospace; font-size: 10px; text-transform: uppercase; padding: 0.35rem 0.75rem; border: 1px solid #333; color: #666; }
.chip.on { background: #39ff14; color: #000; border-color: #000; }
</style>
