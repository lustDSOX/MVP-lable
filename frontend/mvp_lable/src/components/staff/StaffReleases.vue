<template>
  <section class="space-y-4">
    <div class="flex flex-wrap gap-2">
      <button type="button" class="chip" :class="{ on: queueFilter === 'pending' }" @click="queueFilter = 'pending'">Pending</button>
      <button type="button" class="chip" :class="{ on: queueFilter === 'all' }" @click="queueFilter = 'all'">All</button>
    </div>
    <div v-if="!selectedId" class="space-y-3">
      <article v-for="t in filtered" :key="t.id" class="border-2 border-[#333] bg-[#0a0a0a] p-4 cursor-pointer hover:border-[#39FF14]" @click="selectedId = t.id">
        <div class="flex flex-wrap justify-between gap-2">
          <h3 class="font-black uppercase text-lg">{{ t.title }}</h3>
          <span class="font-mono text-[10px] uppercase border border-[#444] px-2 py-0.5">{{ t.status }}</span>
        </div>
        <p class="font-mono text-[10px] text-gray-500 mt-1">{{ t.type || '—' }} · {{ t.artistName || '—' }} · {{ t.createdAt }}</p>
      </article>
      <p v-if="!filtered.length" class="font-mono text-gray-600 text-sm">Ничего не найдено</p>
    </div>
    <div v-else-if="sel" class="space-y-6 border-2 border-[#39FF14] p-4 sm:p-6 bg-[#050505]">
      <div class="flex flex-wrap gap-2 justify-between items-start">
        <button type="button" class="btn-muted" @click="selectedId = null">← К списку</button>
        <span class="font-mono text-xs uppercase text-[#39FF14]">{{ sel.status }}</span>
      </div>
      <h2 class="text-2xl font-black uppercase italic">{{ sel.title }}</h2>
      <div class="grid sm:grid-cols-2 gap-3 font-mono text-xs">
        <p><span class="text-gray-500">TYPE</span> {{ sel.type }}</p>
        <p><span class="text-gray-500">GENRE</span> {{ sel.genre }}</p>
        <p><span class="text-gray-500">DATE</span> {{ sel.releaseDate }}</p>
        <p><span class="text-gray-500">COVER</span> {{ sel.coverNote }}</p>
        <p><span class="text-gray-500">ARTIST</span> {{ sel.artistName }}</p>
        <p><span class="text-gray-500">EMAIL</span> {{ sel.artistEmail }}</p>
        <p><span class="text-gray-500">PHONE</span> {{ sel.artistPhone }}</p>
        <p><span class="text-gray-500">CITY</span> {{ sel.artistCity }}</p>
        <p class="sm:col-span-2"><span class="text-gray-500">SOCIAL</span> {{ sel.socialNetworks }}</p>
      </div>
      <div class="border border-[#333] p-4">
        <p class="font-mono text-xs text-[#39FF14] uppercase mb-2">Договор</p>
        <p class="font-mono text-sm">status: <b>{{ sel.contract?.status }}</b> · v{{ sel.contract?.version }} · signed: {{ sel.contract?.signed ? 'yes' : 'no' }}</p>
        <p class="font-mono text-xs text-gray-500 mt-1">{{ sel.contract?.artistFullName }} · {{ sel.contract?.signedAt || '—' }}</p>
      </div>
      <div class="space-y-4">
        <p class="font-mono text-xs text-[#39FF14] uppercase">Треки ({{ sel.tracksDetail?.length || 0 }})</p>
        <article v-for="tr in sel.tracksDetail || []" :key="tr.localId" class="border border-[#333] p-4 space-y-2">
          <h4 class="font-bold uppercase">#{{ tr.order }} {{ tr.title }} <span v-if="tr.isExplicit" class="text-[#ff0000] text-xs">EXPLICIT</span></h4>
          <p class="font-mono text-[10px] text-gray-500">master: {{ tr.masterFile || '—' }}</p>
          <p class="font-mono text-[10px] text-gray-400">credits: <span v-for="(c, i) in tr.contributors" :key="i"> {{ c.role }}={{ c.creditName }};</span></p>
          <pre class="whitespace-pre-wrap font-mono text-xs text-gray-300 bg-black p-3 border border-[#222] max-h-48 overflow-y-auto">{{ tr.lyrics || '(no lyrics)' }}</pre>
        </article>
      </div>
      <div v-if="sel.moderationLog?.length" class="border border-[#222] p-3">
        <p class="font-mono text-[10px] text-gray-500 uppercase mb-2">Log</p>
        <p v-for="(l, i) in sel.moderationLog" :key="i" class="font-mono text-[10px] text-gray-400">{{ l.at }} · {{ l.action }} · {{ l.by }} <span v-if="l.note">· {{ l.note }}</span></p>
      </div>
      <div class="flex flex-wrap gap-2 pt-2 border-t border-[#333]">
        <button v-if="sel.status === 'pending' || sel.status === 'draft'" type="button" class="btn-green" @click="approve">Approve</button>
        <button v-if="sel.status === 'pending' || sel.status === 'draft'" type="button" class="btn-red" @click="reject">Reject</button>
        <button v-if="sel.status === 'published' || sel.status === 'rejected'" type="button" class="btn-muted" @click="requeue">Вернуть на модерацию</button>
      </div>
    </div>
  </section>
</template>

<script setup lang="ts">
import { computed, ref, watch } from 'vue'
import { useAuthStore } from '@/stores/auth'
import { useTracksStore } from '@/stores/tracks'

const props = defineProps<{ tabQuery: string; focusId?: string | null }>()
const tracks = useTracksStore()
const auth = useAuthStore()
const queueFilter = ref<'pending' | 'all'>('pending')
const selectedId = ref<string | null>(null)

watch(() => props.focusId, (id) => { if (id) selectedId.value = id }, { immediate: true })

const filtered = computed(() => {
  let list = tracks.tracks
  if (queueFilter.value === 'pending') list = list.filter((t) => t.status === 'pending' || t.status === 'draft')
  const q = props.tabQuery.trim().toLowerCase()
  if (q) {
    list = list.filter(
      (t) =>
        t.title.toLowerCase().includes(q) ||
        (t.artistName || '').toLowerCase().includes(q) ||
        t.status.includes(q) ||
        (t.type || '').includes(q),
    )
  }
  return list
})
const sel = computed(() => tracks.tracks.find((t) => t.id === selectedId.value) || null)

function approve() {
  if (!sel.value) return
  tracks.setStatus(sel.value.id, 'published', undefined, auth.email || 'mod')
  selectedId.value = null
}
function reject() {
  if (!sel.value) return
  const reason = window.prompt('Причина отказа', 'Не соответствует гайду')
  if (reason !== null) {
    tracks.setStatus(sel.value.id, 'rejected', reason || 'Rejected', auth.email || 'mod')
    selectedId.value = null
  }
}
function requeue() {
  if (!sel.value) return
  tracks.requeue(sel.value.id, auth.email || 'mod')
}
</script>

<style scoped>
.btn-green { background: #39ff14; color: #000; font-family: 'JetBrains Mono', monospace; font-size: 0.75rem; text-transform: uppercase; padding: 0.5rem 1rem; min-height: 44px; border: 2px solid #000; font-weight: 700; }
.btn-red { background: #ff0000; color: #fff; font-family: 'JetBrains Mono', monospace; font-size: 0.75rem; text-transform: uppercase; padding: 0.5rem 1rem; min-height: 44px; border: 2px solid #000; }
.btn-muted { background: #222; color: #ccc; font-family: 'JetBrains Mono', monospace; font-size: 0.75rem; text-transform: uppercase; padding: 0.5rem 1rem; min-height: 44px; border: 2px solid #444; }
.chip { font-family: 'JetBrains Mono', monospace; font-size: 10px; text-transform: uppercase; padding: 0.35rem 0.75rem; border: 1px solid #333; color: #666; }
.chip.on { background: #39ff14; color: #000; border-color: #000; }
</style>
