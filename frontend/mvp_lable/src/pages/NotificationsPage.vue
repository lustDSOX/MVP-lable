<template>
  <div class="min-h-screen pt-24 px-4 pb-16 text-white font-['Inter',sans-serif]">
    <div class="max-w-6xl mx-auto">
      <div class="flex flex-wrap items-center justify-between gap-3 mb-4 border-b-4 border-[#39FF14] pb-4">
        <h1 class="text-2xl sm:text-3xl font-black uppercase italic">Уведомления</h1>
        <button type="button" class="font-mono text-xs uppercase border border-[#333] px-3 py-2 min-h-[44px]" @click="markAll">Прочитать все</button>
      </div>
      <p v-if="!auth.email" class="font-mono text-sm text-gray-500">Войдите, чтобы видеть уведомления.</p>
      <div v-else class="grid md:grid-cols-[minmax(240px,340px)_1fr] border-2 border-[#333] min-h-[60vh] bg-[#050505]">
        <aside class="border-b md:border-b-0 md:border-r border-[#333] flex flex-col max-h-[40vh] md:max-h-[70vh]">
          <div class="p-3 border-b border-[#333] space-y-2">
            <input v-model="q" type="search" class="w-full bg-black border border-[#333] px-2 py-2 font-mono text-xs" placeholder="Поиск…" />
            <div class="flex gap-1 flex-wrap">
              <button type="button" class="chip" :class="{ on: sort === 'new' }" @click="sort = 'new'">Новые</button>
              <button type="button" class="chip" :class="{ on: sort === 'old' }" @click="sort = 'old'">Старые</button>
              <button type="button" class="chip" :class="{ on: filter === 'all' }" @click="filter = 'all'">Все</button>
              <button type="button" class="chip" :class="{ on: filter === 'unread' }" @click="filter = 'unread'">Непрочит.</button>
            </div>
          </div>
          <div class="overflow-y-auto flex-1">
            <button
              v-for="n in filtered"
              :key="n.id"
              type="button"
              class="w-full text-left px-3 py-3 border-b border-[#222] hover:bg-[#111]"
              :class="{ 'bg-[#0a1a0a] border-l-2 border-l-[#39FF14]': selectedId === n.id, 'opacity-60': n.read }"
              @click="open(n.id)"
            >
              <p class="font-mono text-[10px] uppercase" :class="n.read ? 'text-gray-500' : 'text-[#39FF14]'">{{ n.title }}</p>
              <p class="font-mono text-[9px] text-gray-600 mt-1">{{ fmt(n.createdAt) }}</p>
            </button>
            <p v-if="!filtered.length" class="p-4 font-mono text-xs text-gray-600 text-center">Пусто</p>
          </div>
        </aside>
        <div class="p-4 sm:p-6 overflow-y-auto max-h-[70vh]">
          <template v-if="selected">
            <div class="flex flex-wrap justify-between gap-2 mb-4">
              <h2 class="text-xl font-black uppercase">{{ selected.title }}</h2>
              <span class="font-mono text-[9px] text-gray-500 uppercase">{{ selected.type }}</span>
            </div>
            <p class="font-mono text-[10px] text-gray-600 mb-4">{{ fmt(selected.createdAt) }}</p>
            <p class="text-sm text-gray-200 whitespace-pre-wrap leading-relaxed">{{ selected.body }}</p>
          </template>
          <p v-else class="font-mono text-sm text-gray-600 text-center py-16">Выберите уведомление</p>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed, onMounted, ref, watch } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import { useNotificationsStore } from '@/stores/notifications'

const auth = useAuthStore()
const store = useNotificationsStore()
const route = useRoute()
const router = useRouter()
onMounted(() => store.hydrate())

const q = ref('')
const sort = ref<'new' | 'old'>('new')
const filter = ref<'all' | 'unread'>('all')
const selectedId = ref<string | null>(null)

const list = computed(() => (auth.email ? store.forUser(auth.email) : []))
const filtered = computed(() => {
  let rows = [...list.value]
  if (filter.value === 'unread') rows = rows.filter((n) => !n.read)
  const s = q.value.trim().toLowerCase()
  if (s) rows = rows.filter((n) => n.title.toLowerCase().includes(s) || n.body.toLowerCase().includes(s))
  rows.sort((a, b) => (sort.value === 'new' ? b.createdAt.localeCompare(a.createdAt) : a.createdAt.localeCompare(b.createdAt)))
  return rows
})
const selected = computed(() => list.value.find((n) => n.id === selectedId.value) || null)

function open(id: string) {
  selectedId.value = id
  store.markRead(id)
  router.replace({ query: { ...route.query, id } })
}
function markAll() {
  if (auth.email) store.markAllRead(auth.email)
}
function fmt(iso: string) {
  try { return new Date(iso).toLocaleString() } catch { return iso }
}

watch(
  () => route.query.id,
  (id) => {
    if (typeof id === 'string' && id) {
      selectedId.value = id
      store.markRead(id)
    }
  },
  { immediate: true },
)
</script>

<style scoped>
.chip { font-family: 'JetBrains Mono', monospace; font-size: 9px; text-transform: uppercase; padding: 0.25rem 0.5rem; border: 1px solid #333; color: #666; min-height: 28px; }
.chip.on { background: #39ff14; color: #000; border-color: #000; }
</style>
