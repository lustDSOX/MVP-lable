<template>
  <section class="space-y-4">
    <div class="grid lg:grid-cols-[280px_1fr] gap-4 items-start">
      <div class="border-2 border-[#333] max-h-[70vh] overflow-y-auto">
        <button type="button" class="w-full text-left px-3 py-3 font-mono text-xs border-b border-[#222] text-[#39FF14]" @click="startNew">+ New event</button>
        <button
          v-for="ev in filtered"
          :key="ev.id"
          type="button"
          class="w-full text-left px-3 py-3 border-b border-[#222] hover:bg-[#111]"
          :class="selectedId === ev.id ? 'bg-[#111] border-l-4 border-l-[#39FF14]' : ''"
          @click="select(ev)"
        >
          <p class="font-mono text-xs uppercase text-white truncate">{{ ev.title }}</p>
          <p class="font-mono text-[9px] text-gray-500">{{ ev.status }} · {{ ev.date }} · {{ ev.city }}</p>
        </button>
      </div>
      <div class="border-2 border-[#333] p-4 space-y-3">
        <template v-if="selectedId || creating || form.title">
          <p class="font-mono text-xs text-[#39FF14] uppercase">{{ editingId ? 'Edit event' : 'New event' }}</p>
          <input v-model="form.title" required placeholder="TITLE" class="field" />
          <div class="grid sm:grid-cols-2 gap-2">
            <input v-model="form.venue" placeholder="VENUE" class="field" />
            <input v-model="form.city" placeholder="CITY" class="field" />
            <input v-model="form.date" placeholder="15 AUG" class="field" />
            <input v-model="form.time" placeholder="23:00" class="field" />
            <input v-model="form.price" placeholder="PRICE" class="field" />
            <input v-model="form.capacity" placeholder="CAPACITY" class="field" />
            <input v-model="form.ageLimit" placeholder="AGE 18+" class="field" />
            <input v-model="form.ticketUrl" placeholder="TICKET URL" class="field" />
          </div>
          <textarea v-model="form.description" rows="3" placeholder="DESC" class="field" />
          <select v-model="form.status" class="field">
            <option value="draft">draft</option>
            <option value="published">published</option>
          </select>
          <div class="flex flex-wrap gap-2">
            <button type="button" class="btn-green" @click="save">Save</button>
            <a v-if="form.ticketUrl" :href="form.ticketUrl" class="btn-muted inline-flex items-center" target="_blank" rel="noopener">Открыть оплату</a>
            <button v-if="editingId" type="button" class="btn-red" @click="remove">Del</button>
            <button type="button" class="btn-muted" @click="reset">Clear</button>
          </div>
        </template>
        <p v-else class="font-mono text-sm text-gray-500">Выбери событие слева или создай новое</p>
      </div>
    </div>
  </section>
</template>

<script setup lang="ts">
import { computed, reactive, ref, watch } from 'vue'
import { useCmsStore, type EventItem } from '@/stores/cms'

const props = defineProps<{ tabQuery: string; focusId?: string | null }>()
const cms = useCmsStore()
const selectedId = ref<string | null>(null)
const editingId = ref<string | null>(null)
const creating = ref(false)
const form = reactive({
  title: '',
  venue: '',
  city: '',
  date: '15 AUG',
  time: '23:00',
  description: '',
  status: 'draft' as 'draft' | 'published',
  ticketUrl: '/purchase',
  price: '',
  capacity: '',
  ageLimit: '18+',
})

watch(
  () => props.focusId,
  (id) => {
    if (!id) return
    const ev = cms.events.find((e) => e.id === id)
    if (ev) select(ev)
  },
  { immediate: true },
)

const filtered = computed(() => {
  const q = props.tabQuery.trim().toLowerCase()
  if (!q) return cms.events
  return cms.events.filter(
    (e) =>
      e.title.toLowerCase().includes(q) ||
      e.city.toLowerCase().includes(q) ||
      e.venue.toLowerCase().includes(q) ||
      e.description.toLowerCase().includes(q),
  )
})

function reset() {
  editingId.value = null
  selectedId.value = null
  creating.value = false
  form.title = ''
  form.venue = ''
  form.city = ''
  form.date = '15 AUG'
  form.time = '23:00'
  form.description = ''
  form.status = 'draft'
  form.ticketUrl = '/purchase'
  form.price = ''
  form.capacity = ''
  form.ageLimit = '18+'
}
function startNew() {
  reset()
  creating.value = true
}
function select(ev: EventItem) {
  selectedId.value = ev.id
  editingId.value = ev.id
  creating.value = false
  form.title = ev.title
  form.venue = ev.venue
  form.city = ev.city
  form.date = ev.date
  form.time = ev.time
  form.description = ev.description
  form.status = ev.status
  form.ticketUrl = ev.ticketUrl || '/purchase'
  form.price = ev.price || ''
  form.capacity = ev.capacity || ''
  form.ageLimit = ev.ageLimit || '18+'
}
function save() {
  cms.upsertEvent({
    id: editingId.value || undefined,
    title: form.title,
    venue: form.venue,
    city: form.city,
    date: form.date,
    time: form.time,
    description: form.description,
    status: form.status,
    ticketUrl: form.ticketUrl,
    price: form.price,
    capacity: form.capacity,
    ageLimit: form.ageLimit,
  })
  reset()
}
function remove() {
  if (editingId.value) {
    cms.deleteEvent(editingId.value)
    reset()
  }
}
</script>

<style scoped>
.field { display: block; width: 100%; background: #000; border: 2px solid #333; color: #fff; padding: 0.75rem; font-family: 'JetBrains Mono', monospace; font-size: 0.875rem; }
.btn-green { background: #39ff14; color: #000; font-family: 'JetBrains Mono', monospace; font-size: 0.75rem; text-transform: uppercase; padding: 0.5rem 1rem; min-height: 44px; border: 2px solid #000; font-weight: 700; }
.btn-red { background: #ff0000; color: #fff; font-family: 'JetBrains Mono', monospace; font-size: 0.75rem; text-transform: uppercase; padding: 0.5rem 1rem; min-height: 44px; border: 2px solid #000; }
.btn-muted { background: #222; color: #ccc; font-family: 'JetBrains Mono', monospace; font-size: 0.75rem; text-transform: uppercase; padding: 0.5rem 1rem; min-height: 44px; border: 2px solid #444; }
</style>
