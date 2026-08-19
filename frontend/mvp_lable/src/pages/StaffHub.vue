<template>
  <div class="min-h-screen pt-24 px-4 pb-16 text-white font-['Inter',sans-serif]">
    <div class="max-w-5xl mx-auto">
      <header class="border-b-4 border-[#39FF14] pb-4 mb-6">
        <p class="font-mono text-[10px] text-gray-500 uppercase tracking-widest mb-1">Staff_Cabinet // role-based</p>
        <h1 class="text-3xl sm:text-4xl font-black uppercase italic tracking-tight">{{ auth.artistName || 'STAFF' }}</h1>
        <div class="mt-3 flex flex-wrap gap-2 items-center">
          <span class="font-mono text-xs px-2 py-1 bg-[#39FF14] text-black font-bold uppercase">{{ auth.role }}</span>
          <span class="font-mono text-[10px] text-gray-500">{{ auth.email }}</span>
          <span v-for="p in myPerms" :key="p" class="font-mono text-[9px] border border-[#333] text-gray-400 px-2 py-0.5 uppercase">{{ p }}</span>
        </div>
      </header>

      <div class="mb-6 space-y-2">
        <input v-model="globalQuery" type="search" placeholder="Поиск по всему кабинету…" class="field" />
        <div v-if="globalQuery.trim() && globalHits.length" class="border border-[#333] bg-[#0a0a0a] p-3 space-y-2 max-h-48 overflow-y-auto">
          <button v-for="(h, i) in globalHits" :key="i" type="button" class="block w-full text-left font-mono text-xs text-gray-300 hover:text-[#39FF14] py-1" @click="goHit(h)">
            <span class="text-[#39FF14]">{{ h.tab }}</span> · {{ h.label }}
          </button>
        </div>
        <input v-if="active" v-model="tabQuery" type="search" :placeholder="`Поиск в «${activeLabel}»…`" class="field" />
      </div>

      <div v-if="availableTabs.length" class="flex flex-wrap gap-2 mb-8">
        <button v-for="tab in availableTabs" :key="tab.id" type="button" class="min-h-[44px] px-4 font-mono text-xs uppercase border-2" :class="active === tab.id ? 'bg-[#39FF14] text-black border-black' : 'border-[#333] text-gray-400'" @click="switchTab(tab.id)">{{ tab.label }}</button>
      </div>
      <p v-else class="font-mono text-sm text-[#ff0000] mb-8">Нет выданных прав.</p>

      <StaffReleases v-if="active === 'releases'" :tab-query="tabQuery" :focus-id="focusReleaseId" />
      <StaffNews v-else-if="active === 'news'" :tab-query="tabQuery" :focus-id="focusNewsId" />
      <StaffGuides v-else-if="active === 'guides'" :tab-query="tabQuery" :focus-id="focusGuideId" />
      <StaffEvents v-else-if="active === 'events'" :tab-query="tabQuery" :focus-id="focusEventId" />
      <StaffMatrix v-else-if="active === 'matrix'" :tab-query="tabQuery" />
      <StaffUsers v-else-if="active === 'users'" :tab-query="tabQuery" />
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed, onMounted, ref, watch } from 'vue'
import { useAuthStore } from '@/stores/auth'
import { useCmsStore } from '@/stores/cms'
import { usePermissionsStore } from '@/stores/permissions'
import { useTracksStore } from '@/stores/tracks'
import { useAdminStore } from '@/stores/admin'
import StaffReleases from '@/components/staff/StaffReleases.vue'
import StaffNews from '@/components/staff/StaffNews.vue'
import StaffEvents from '@/components/staff/StaffEvents.vue'
import StaffMatrix from '@/components/staff/StaffMatrix.vue'
import StaffUsers from '@/components/staff/StaffUsers.vue'
import StaffGuides from '@/components/staff/StaffGuides.vue'

const auth = useAuthStore()
const cms = useCmsStore()
const perm = usePermissionsStore()
const tracks = useTracksStore()
const admin = useAdminStore()
const myPerms = computed(() => auth.myPermissions())

const active = ref('')
const globalQuery = ref('')
const tabQuery = ref('')
const focusNewsId = ref<string | null>(null)
const focusEventId = ref<string | null>(null)
const focusReleaseId = ref<string | null>(null)
const focusGuideId = ref<string | null>(null)

const availableTabs = computed(() => {
  const tabs: { id: string; label: string }[] = []
  if (auth.can('releases.moderate')) tabs.push({ id: 'releases', label: 'Релизы' })
  if (auth.can('news.manage')) tabs.push({ id: 'news', label: 'Новости' })
  if (auth.can('events.manage')) tabs.push({ id: 'events', label: 'События' })
  if (auth.can('guides.manage')) tabs.push({ id: 'guides', label: 'Гайды' })
  if (auth.can('permissions.manage')) tabs.push({ id: 'matrix', label: 'Matrix' })
  if (auth.can('users.manage')) tabs.push({ id: 'users', label: 'Аккаунты' })
  return tabs
})
const activeLabel = computed(() => availableTabs.value.find((t) => t.id === active.value)?.label || '')

watch(availableTabs, (tabs) => {
  if (!tabs.find((t) => t.id === active.value)) active.value = tabs[0]?.id || ''
}, { immediate: true })

function switchTab(id: string) {
  active.value = id
  tabQuery.value = ''
  focusNewsId.value = null
  focusEventId.value = null
  focusReleaseId.value = null
  focusGuideId.value = null
}

type Hit = { tab: string; label: string; tabId: string; id?: string }
const globalHits = computed((): Hit[] => {
  const q = globalQuery.value.trim().toLowerCase()
  if (!q) return []
  const hits: Hit[] = []
  if (auth.can('releases.moderate')) {
    for (const t of tracks.tracks) {
      if (t.title.toLowerCase().includes(q) || (t.artistName || '').toLowerCase().includes(q))
        hits.push({ tab: 'Релизы', tabId: 'releases', label: t.title, id: t.id })
    }
  }
  if (auth.can('news.manage')) {
    for (const n of cms.news) {
      if (n.title.toLowerCase().includes(q) || n.body.toLowerCase().includes(q))
        hits.push({ tab: 'Новости', tabId: 'news', label: n.title, id: n.id })
    }
  }
  if (auth.can('events.manage')) {
    for (const e of cms.events) {
      if (e.title.toLowerCase().includes(q) || e.city.toLowerCase().includes(q))
        hits.push({ tab: 'События', tabId: 'events', label: e.title, id: e.id })
    }
  }
  if (auth.can('guides.manage')) {
    for (const g of cms.guides) {
      if (g.title.toLowerCase().includes(q) || g.body.toLowerCase().includes(q))
        hits.push({ tab: 'Гайды', tabId: 'guides', label: g.title, id: g.id })
    }
  }
  if (auth.can('users.manage')) {
    for (const u of admin.users) {
      if (u.email.toLowerCase().includes(q) || u.name.toLowerCase().includes(q))
        hits.push({ tab: 'Аккаунты', tabId: 'users', label: `${u.name} <${u.email}>`, id: u.id })
    }
  }
  return hits.slice(0, 20)
})

function goHit(h: Hit) {
  active.value = h.tabId
  tabQuery.value = ''
  globalQuery.value = ''
  focusNewsId.value = h.tabId === 'news' ? h.id || null : null
  focusEventId.value = h.tabId === 'events' ? h.id || null : null
  focusReleaseId.value = h.tabId === 'releases' ? h.id || null : null
  focusGuideId.value = h.tabId === 'guides' ? h.id || null : null
}

onMounted(() => {
  cms.hydrate()
  perm.hydrate()
  admin.hydrate()
  tracks.fetchTracks()
})
</script>

<style scoped>
.field {
  display: block;
  width: 100%;
  background: #000;
  border: 2px solid #333;
  color: #fff;
  padding: 0.75rem;
  font-family: 'JetBrains Mono', monospace;
  font-size: 0.875rem;
}
</style>
