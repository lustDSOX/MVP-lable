<template>
  <section class="space-y-4">
    <div class="flex flex-wrap gap-2">
      <button type="button" class="chip" :class="{ on: queueFilter === 'pending' }" @click="queueFilter = 'pending'">Pending</button>
      <button type="button" class="chip" :class="{ on: queueFilter === 'all' }" @click="queueFilter = 'all'">All</button>
    </div>

    <div v-if="!selectedId" class="space-y-3">
      <article
        v-for="t in filtered"
        :key="t.id"
        class="border-2 border-[#333] bg-[#0a0a0a] p-4 cursor-pointer hover:border-[#39FF14]"
        @click="openRelease(t.id)"
      >
        <div class="flex flex-wrap justify-between gap-2">
          <h3 class="font-black uppercase text-lg">{{ t.title }}</h3>
          <span class="font-mono text-[10px] uppercase border border-[#444] px-2 py-0.5">{{ t.status }}</span>
        </div>
        <p class="font-mono text-[10px] text-gray-500 mt-1">{{ t.type || '—' }} · {{ t.artistName || '—' }} · {{ t.createdAt }}</p>
      </article>
      <p v-if="!filtered.length" class="font-mono text-gray-600 text-sm">Ничего не найдено</p>
    </div>

    <div v-else-if="sel && !trackView" ref="detailEl" class="space-y-6 border-2 border-[#39FF14] p-4 sm:p-6 bg-[#050505] pb-28">
      <div class="flex flex-wrap gap-2 justify-between items-start">
        <h2 class="text-2xl font-black uppercase italic">{{ sel.title }}</h2>
        <span class="font-mono text-xs uppercase text-[#39FF14]">{{ sel.status }}</span>
      </div>
      <div class="form-actions-fixed">
        <button type="button" class="btn-muted" @click="selectedId = null">← К списку</button>
        <button v-if="sel.status === 'pending' || sel.status === 'draft'" type="button" class="btn-green" @click="approve">Одобрить</button>
        <button v-if="sel.status === 'pending' || sel.status === 'draft'" type="button" class="btn-red" @click="rejectOpen = true">Отклонить</button>
        <button v-if="sel.status === 'published' || sel.status === 'rejected'" type="button" class="btn-muted" @click="requeue">На модерацию</button>
      </div>

      <div class="grid sm:grid-cols-[180px_1fr] gap-4">
        <div>
          <p class="lbl mb-2">Обложка</p>
          <img v-if="sel.coverUrl" :src="sel.coverUrl" alt="cover" class="w-full aspect-square object-cover border-2 border-[#333]" />
          <div class="flex flex-wrap gap-2 mt-2">
            <button v-if="sel.coverUrl" type="button" class="btn-muted" @click="openInNewTab(sel.coverUrl!)">Открыть</button>
            <button v-if="sel.coverUrl" type="button" class="btn-muted" @click="forceDownload(sel.coverUrl!, `${sel.title}-cover.jpg`)">Скачать</button>
          </div>
          <p class="font-mono text-[10px] text-gray-500 mt-1">{{ sel.coverNote }}</p>
        </div>
        <div class="grid sm:grid-cols-2 gap-3 font-mono text-xs content-start">
          <p><span class="text-gray-500">Тип</span><br />{{ sel.type }}</p>
          <p><span class="text-gray-500">Жанр</span><br />{{ sel.genre }}</p>
          <p><span class="text-gray-500">Дата</span><br />{{ sel.releaseDate }}</p>
          <p><span class="text-gray-500">Артист</span><br />{{ sel.artistName }}</p>
          <p><span class="text-gray-500">Email</span><br />{{ sel.artistEmail }}</p>
          <p><span class="text-gray-500">Телефон</span><br />{{ sel.artistPhone }}</p>
          <p><span class="text-gray-500">Город</span><br />{{ sel.artistCity }}</p>
          <p><span class="text-gray-500">Соцсети</span><br />{{ sel.socialNetworks }}</p>
        </div>
      </div>

      <div class="border border-[#333] p-4 space-y-2">
        <p class="font-mono text-xs text-[#39FF14] uppercase">Договор</p>
        <p class="font-mono text-sm">Статус: <b>{{ sel.contract?.status }}</b> · v{{ sel.contract?.version }} · {{ sel.contract?.signed ? 'подписан' : 'нет' }}</p>
        <p class="font-mono text-xs text-gray-500">{{ sel.contract?.artistFullName }} · {{ sel.contract?.signedAt || '—' }}</p>
        <div class="flex gap-2 flex-wrap">
          <button v-if="sel.contractPdfUrl" type="button" class="btn-muted" @click="openInNewTab(sel.contractPdfUrl!)">Открыть PDF</button>
          <button v-if="sel.contractPdfUrl" type="button" class="btn-muted" @click="forceDownload(sel.contractPdfUrl!, `${sel.title}-contract.pdf`)">Скачать PDF</button>
        </div>
      </div>

      <div class="space-y-2">
        <p class="font-mono text-xs text-[#39FF14] uppercase">Треки — открой для Genius-вида</p>
        <button
          v-for="tr in sel.tracksDetail || []"
          :key="tr.localId"
          type="button"
          class="w-full text-left border border-[#333] p-3 hover:border-[#39FF14] flex justify-between gap-2"
          @click="trackViewId = tr.localId"
        >
          <span class="font-bold uppercase">#{{ tr.order }} {{ tr.title }}
            <span v-if="tr.isExplicit" class="text-[#ff0000] text-xs">EXPLICIT</span>
          </span>
          <span class="font-mono text-[10px] text-gray-500">→</span>
        </button>
      </div>
    </div>

    <div v-else-if="sel && trackView" class="space-y-4 border-2 border-[#39FF14] p-4 sm:p-6 bg-[#050505] pb-28">
      <h2 class="text-3xl font-black uppercase italic">{{ trackView.title }}</h2>
      <div class="form-actions-fixed">
        <button type="button" class="btn-muted" @click="trackViewId = null">← К релизу</button>
      </div>
      <p class="font-mono text-xs text-gray-400" v-for="(c, i) in trackView.contributors" :key="i">{{ c.role }}: <span class="text-white">{{ c.creditName }}</span></p>
      <div v-if="trackView.audioUrl">
        <p class="lbl mb-2">Плеер</p>
        <AudioPlayer :src="trackView.audioUrl" :title="trackView.title" subtitle="preview" />
      </div>
      <pre class="whitespace-pre-wrap font-serif text-lg leading-relaxed text-gray-100 border border-[#333] p-4 bg-black">{{ trackView.lyrics || '(нет текста)' }}</pre>
    </div>

    <ReasonModal
      :open="rejectOpen"
      title="Отклонение релиза"
      hint="Причина уйдёт на email артиста (mock)."
      initial="Не соответствует гайду"
      @cancel="rejectOpen = false"
      @confirm="confirmReject"
    />
  </section>
</template>

<script setup lang="ts">
import { computed, nextTick, ref, watch } from 'vue'
import { useAuthStore } from '@/stores/auth'
import { useTracksStore } from '@/stores/tracks'
import { forceDownload, openInNewTab } from '@/utils/download'
import ReasonModal from './ReasonModal.vue'
import AudioPlayer from '@/components/ui/AudioPlayer.vue'

const props = defineProps<{ tabQuery: string; focusId?: string | null }>()
const tracks = useTracksStore()
const auth = useAuthStore()
const queueFilter = ref<'pending' | 'all'>('pending')
const selectedId = ref<string | null>(null)
const trackViewId = ref<string | null>(null)
const rejectOpen = ref(false)
const detailEl = ref<HTMLElement | null>(null)

watch(() => props.focusId, (id) => { if (id) openRelease(id) }, { immediate: true })

const filtered = computed(() => {
  let list = tracks.tracks
  if (queueFilter.value === 'pending') list = list.filter((t) => t.status === 'pending' || t.status === 'draft')
  const q = props.tabQuery.trim().toLowerCase()
  if (q) {
    list = list.filter(
      (t) =>
        t.title.toLowerCase().includes(q) ||
        (t.artistName || '').toLowerCase().includes(q) ||
        t.status.includes(q),
    )
  }
  return list
})
const sel = computed(() => tracks.tracks.find((t) => t.id === selectedId.value) || null)
const trackView = computed(() => sel.value?.tracksDetail?.find((t) => t.localId === trackViewId.value) || null)

async function openRelease(id: string) {
  selectedId.value = id
  trackViewId.value = null
  await nextTick()
  detailEl.value?.scrollIntoView({ behavior: 'smooth', block: 'start' })
}

function approve() {
  if (!sel.value) return
  tracks.setStatus(sel.value.id, 'published', undefined, auth.email || 'mod')
  selectedId.value = null
}
function confirmReject(reason: string) {
  if (!sel.value) return
  tracks.setStatus(sel.value.id, 'rejected', reason, auth.email || 'mod')
  rejectOpen.value = false
  selectedId.value = null
}
function requeue() {
  if (!sel.value) return
  tracks.requeue(sel.value.id, auth.email || 'mod')
}
</script>

<style scoped>
.lbl { font-family: 'JetBrains Mono', monospace; font-size: 10px; text-transform: uppercase; color: #9ca3af; }
.btn-green { background: #39ff14; color: #000; font-family: 'JetBrains Mono', monospace; font-size: 0.75rem; text-transform: uppercase; padding: 0.5rem 1rem; min-height: 44px; border: 2px solid #000; font-weight: 700; }
.btn-red { background: #ff0000; color: #fff; font-family: 'JetBrains Mono', monospace; font-size: 0.75rem; text-transform: uppercase; padding: 0.5rem 1rem; min-height: 44px; border: 2px solid #000; }
.btn-muted { background: #222; color: #ccc; font-family: 'JetBrains Mono', monospace; font-size: 0.75rem; text-transform: uppercase; padding: 0.5rem 1rem; min-height: 44px; border: 2px solid #444; display: inline-block; }
.chip { font-family: 'JetBrains Mono', monospace; font-size: 10px; text-transform: uppercase; padding: 0.35rem 0.75rem; border: 1px solid #333; color: #666; }
.chip.on { background: #39ff14; color: #000; border-color: #000; }
.form-actions-fixed {
  position: fixed;
  left: 0;
  right: 0;
  bottom: 0;
  z-index: 60;
  display: flex;
  flex-wrap: wrap;
  gap: 0.5rem;
  padding: 0.75rem 1rem calc(0.75rem + env(safe-area-inset-bottom));
  background: rgba(0, 0, 0, 0.96);
  border-top: 2px solid #39ff14;
  box-shadow: 0 -4px 20px rgba(0,0,0,0.6);
  justify-content: center;
}
</style>
