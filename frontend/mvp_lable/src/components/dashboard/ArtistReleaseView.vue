<template>
  <section v-if="track" class="space-y-4 border-2 border-[#39FF14] bg-[#050505] p-4 sm:p-6">
    <div class="flex flex-wrap items-start justify-between gap-3">
      <div>
        <button type="button" class="btn-muted mb-2" @click="$emit('close')">← К списку</button>
        <h2 class="text-2xl sm:text-3xl font-black uppercase italic">{{ track.title }}</h2>
        <p class="font-mono text-xs text-gray-500 mt-1">{{ track.type || '—' }} · {{ track.status }} · {{ track.createdAt }}</p>
      </div>
      <span class="font-mono text-[10px] uppercase border-2 px-2 py-1" :class="statusClass">{{ track.status }}</span>
    </div>

    <div v-if="track.status === 'rejected' && track.rejectReason" class="border-2 border-[#ff0000] bg-[#1a0000] p-4">
      <p class="font-mono text-[10px] text-[#ff0000] uppercase mb-1">Замечания модерации</p>
      <p class="text-sm text-gray-200">{{ track.rejectReason }}</p>
    </div>
    <div v-if="track.status === 'changes_requested'" class="border-2 border-[#f97316] bg-[#1a0a00] p-4">
      <p class="font-mono text-[10px] text-[#f97316] uppercase mb-1">Лейбл просит правки</p>
      <p class="text-sm text-gray-200">{{ track.changeRequestNote || track.rejectReason || 'См. историю' }}</p>
    </div>
    <div v-if="track.liveRevision && track.status === 'pending'" class="border-2 border-[#facc15] bg-[#1a1500] p-4">
      <p class="font-mono text-[10px] text-[#facc15] uppercase mb-1">LIVE_REVISION на проверке</p>
      <p class="text-sm text-gray-300">Опубликованный релиз повторно на модерации (mock).</p>
    </div>
    <div v-if="track.contract?.status === 'needs_resign'" class="border-2 border-[#facc15] bg-[#1a1500] p-4">
      <p class="font-mono text-[10px] text-[#facc15] uppercase mb-1">Переподписание договора</p>
      <button type="button" class="btn-green" @click="resign">Переподписать</button>
    </div>

    <div class="flex flex-wrap gap-2 border-b border-[#333] pb-2">
      <button v-for="t in tabs" :key="t.id" type="button" class="tab" :class="{ on: tab === t.id }" @click="tab = t.id">{{ t.label }}</button>
    </div>

    <div v-if="tab === 'view'" class="space-y-4">
      <div class="grid sm:grid-cols-[160px_1fr] gap-4">
        <img v-if="track.coverUrl" :src="track.coverUrl" alt="cover" class="w-full aspect-square object-cover border-2 border-[#333]" />
        <div class="grid sm:grid-cols-2 gap-2 font-mono text-xs">
          <p><span class="text-gray-500">Жанр</span><br />{{ track.genre || '—' }}</p>
          <p><span class="text-gray-500">Дата</span><br />{{ track.releaseDate || '—' }}</p>
          <p><span class="text-gray-500">Артист</span><br />{{ track.artistName || '—' }}</p>
          <p><span class="text-gray-500">Договор</span><br />{{ track.contract?.status || '—' }}</p>
        </div>
      </div>
      <button v-for="tr in track.tracksDetail || []" :key="tr.localId" type="button" class="w-full text-left border border-[#333] p-3 mb-2 hover:border-[#39FF14]" @click="listenId = tr.localId; tab = 'listen'">
        <span class="font-bold uppercase">#{{ tr.order }} {{ tr.title }}</span>
      </button>
    </div>

    <div v-else-if="tab === 'listen'" class="space-y-4">
      <div class="flex flex-wrap gap-2">
        <button v-for="tr in track.tracksDetail || []" :key="tr.localId" type="button" class="chip" :class="{ on: listenId === tr.localId }" @click="listenId = tr.localId">#{{ tr.order }} {{ tr.title }}</button>
      </div>
      <template v-if="listenTrack">
        <AudioPlayer v-if="listenTrack.audioUrl" :src="listenTrack.audioUrl" :title="listenTrack.title" />
        <pre class="whitespace-pre-wrap font-mono text-sm text-gray-200 border border-[#333] p-4 bg-black">{{ listenTrack.lyrics || '(no lyrics)' }}</pre>
      </template>
    </div>

    <div v-else-if="tab === 'stats'" class="space-y-4">
      <div class="grid grid-cols-2 sm:grid-cols-4 gap-3">
        <div class="stat"><span class="lbl">Plays</span><span class="val">{{ (track.plays || 0).toLocaleString() }}</span></div>
        <div class="stat"><span class="lbl">Royalties</span><span class="val">${{ track.royalties || 0 }}</span></div>
      </div>
      <div v-for="(v, k) in track.platforms" :key="k" class="border border-[#333] p-3 flex justify-between font-mono text-xs">
        <span class="uppercase text-gray-400">{{ k }}</span><span>{{ Number(v).toLocaleString() }}</span>
      </div>
    </div>

    <div v-else-if="tab === 'history'" class="space-y-2">
      <article v-for="(h, i) in historySorted" :key="i" class="border border-[#333] p-3 font-mono text-xs">
        <div class="flex justify-between text-gray-500"><span>{{ formatAt(h.at) }}</span><span class="text-[#39FF14]">{{ h.kind || 'system' }} · {{ h.action }}</span></div>
        <p class="text-gray-300 mt-1">by {{ h.by }}</p>
        <p v-if="h.note" class="text-white mt-1">{{ h.note }}</p>
      </article>
    </div>

    <div v-else-if="tab === 'edit'" class="space-y-4">
      <p class="font-mono text-[10px] text-gray-500">Правки published → модерация + LIVE_REVISION</p>
      <label class="block"><span class="lbl">Название</span><input v-model="form.title" class="field" /></label>
      <div class="grid sm:grid-cols-2 gap-3">
        <label class="block"><span class="lbl">Тип</span>
          <select v-model="form.type" class="field"><option value="single">single</option><option value="ep">ep</option><option value="album">album</option></select>
        </label>
        <label class="block"><span class="lbl">Жанр</span><input v-model="form.genre" class="field" /></label>
        <label class="block"><span class="lbl">Дата</span><input v-model="form.releaseDate" type="date" class="field" /></label>
      </div>
      <div v-for="(tr, idx) in form.tracks" :key="tr.localId" class="border border-[#333] p-4 space-y-3">
        <p class="font-mono text-xs text-[#39FF14] uppercase">Трек #{{ idx + 1 }}</p>
        <label class="block"><span class="lbl">Название</span><input v-model="tr.title" class="field" /></label>
        <label class="flex items-center gap-2 font-mono text-xs"><input type="checkbox" v-model="tr.isExplicit" class="accent-[#39FF14]" /> Explicit</label>
        <div>
          <span class="lbl">Текст — шаблоны</span>
          <div class="flex flex-wrap gap-1 mt-1 mb-2">
            <button v-for="tpl in lyricTemplates" :key="tpl.label" type="button" class="tool" @click="insertLyrics(idx, tpl.text)">{{ tpl.label }}</button>
          </div>
          <textarea v-model="tr.lyrics" rows="8" class="field font-mono text-sm" />
        </div>
        <AudioPlayer v-if="tr.audioUrl" :src="tr.audioUrl" :title="tr.title" />
      </div>
      <div class="flex flex-wrap gap-2 sticky bottom-0 bg-[#050505] py-3 border-t border-[#333]">
        <button type="button" class="btn-green" @click="save">Сохранить</button>
        <button type="button" class="btn-muted" @click="submitAgain" v-if="track.status !== 'pending'">На модерацию</button>
      </div>
      <p v-if="saveMsg" class="font-mono text-xs text-[#39FF14]">{{ saveMsg }}</p>
    </div>
  </section>
</template>

<script setup lang="ts">
import { computed, reactive, ref, watch } from 'vue'
import { useAuthStore } from '@/stores/auth'
import { useNotificationsStore } from '@/stores/notifications'
import { useTracksStore, type Track } from '@/stores/tracks'
import AudioPlayer from '@/components/ui/AudioPlayer.vue'

const props = defineProps<{ trackId: string }>()
defineEmits<{ close: [] }>()

const tracks = useTracksStore()
const auth = useAuthStore()
const notif = useNotificationsStore()
notif.hydrate()
const tab = ref<'view' | 'listen' | 'stats' | 'history' | 'edit'>('view')
const listenId = ref<string | null>(null)
const saveMsg = ref('')

const tabs = [
  { id: 'view' as const, label: 'Обзор' },
  { id: 'listen' as const, label: 'Слушать' },
  { id: 'stats' as const, label: 'Статистика' },
  { id: 'history' as const, label: 'История' },
  { id: 'edit' as const, label: 'Редактировать' },
]

const lyricTemplates = [
  { label: 'Куплет', text: '\n[VERSE — Artist]\n' },
  { label: 'Припев', text: '\n[CHORUS — Artist]\n' },
  { label: 'Бридж', text: '\n[BRIDGE — Artist]\n' },
  { label: 'Интро', text: '\n[INTRO]\n' },
  { label: 'Аутро', text: '\n[OUTRO]\n' },
  { label: 'Кто поёт', text: '\n[VOCAL — Name / role]\n' },
]

const track = computed(() => tracks.tracks.find((t) => t.id === props.trackId) || null)
const statusClass = computed(() => {
  const s = track.value?.status
  if (s === 'rejected') return 'border-[#ff0000] text-[#ff0000]'
  if (s === 'published') return 'border-[#39FF14] text-[#39FF14]'
  if (s === 'pending') return 'border-[#facc15] text-[#facc15]'
  if (s === 'changes_requested') return 'border-[#f97316] text-[#f97316]'
  return 'border-[#444] text-gray-400'
})
const historySorted = computed(() => [...(track.value?.moderationLog || [])].reverse())
const listenTrack = computed(() => track.value?.tracksDetail?.find((t) => t.localId === listenId.value) || track.value?.tracksDetail?.[0] || null)

const form = reactive({
  title: '',
  type: 'single' as string,
  genre: '',
  releaseDate: '',
  tracks: [] as NonNullable<Track['tracksDetail']>,
})

function syncForm() {
  const t = track.value
  if (!t) return
  form.title = t.title
  form.type = t.type || 'single'
  form.genre = t.genre || ''
  form.releaseDate = t.releaseDate || ''
  form.tracks = JSON.parse(JSON.stringify(t.tracksDetail || []))
  if (!listenId.value && form.tracks[0]) listenId.value = form.tracks[0].localId
}
watch(track, syncForm, { immediate: true })

function insertLyrics(idx: number, text: string) {
  const tr = form.tracks[idx]
  if (!tr) return
  tr.lyrics = (tr.lyrics || '') + text
}

function save() {
  if (!track.value) return
  const { needsResign } = tracks.updateRelease(
    track.value.id,
    {
      title: form.title,
      type: form.type as Track['type'],
      genre: form.genre,
      releaseDate: form.releaseDate,
      tracksDetail: form.tracks,
    },
    auth.email || 'artist',
  )
  if (needsResign) {
    saveMsg.value = 'Сохранено. Нужен re-sign договора.'
    tab.value = 'view'
  } else if (track.value?.liveRevision || track.value?.status === 'pending') {
    saveMsg.value = 'Сохранено. На проверке (LIVE_REVISION).'
  } else {
    saveMsg.value = 'Сохранено.'
  }
}

function submitAgain() {
  save()
  if (!track.value) return
  if (track.value.contract?.status === 'needs_resign' || !track.value.contractSigned) {
    saveMsg.value = 'Сначала переподпишите договор.'
    return
  }
  tracks.completeTrackUpload(track.value.id)
  const live = !!track.value.liveRevision
  for (const e of ['moderator@label.ru', 'manager@label.ru', 'staff@label.ru', 'admin@label.ru']) {
    notif.notifyUser(
      e,
      live ? 'LIVE revision на проверке' : 'Новый релиз на проверке',
      `«${track.value.title}» от ${auth.email || 'artist'}`,
      'release_pending',
    )
  }
  saveMsg.value = 'Отправлено на модерацию.'
  tab.value = 'history'
}

function resign() {
  if (!track.value) return
  tracks.resignContract(track.value.id, auth.artistName || 'Artist', auth.email || 'artist')
  saveMsg.value = 'Договор переподписан (mock).'
}

function formatAt(iso: string) {
  try { return new Date(iso).toLocaleString() } catch { return iso }
}
</script>

<style scoped>
.tab { font-family: 'JetBrains Mono', monospace; font-size: 10px; text-transform: uppercase; padding: 0.5rem 0.75rem; border: 1px solid #333; color: #888; min-height: 40px; }
.tab.on { background: #39ff14; color: #000; border-color: #000; font-weight: 700; }
.lbl { font-family: 'JetBrains Mono', monospace; font-size: 10px; text-transform: uppercase; color: #9ca3af; display: block; margin-bottom: 0.25rem; }
.field { display: block; width: 100%; background: #000; border: 2px solid #333; color: #fff; padding: 0.75rem; font-family: 'JetBrains Mono', monospace; font-size: 0.875rem; }
.btn-green { background: #39ff14; color: #000; font-family: 'JetBrains Mono', monospace; font-size: 0.75rem; text-transform: uppercase; padding: 0.5rem 1rem; min-height: 44px; border: 2px solid #000; font-weight: 700; }
.btn-muted { background: #222; color: #ccc; font-family: 'JetBrains Mono', monospace; font-size: 0.75rem; text-transform: uppercase; padding: 0.5rem 1rem; min-height: 44px; border: 2px solid #444; }
.chip { font-family: 'JetBrains Mono', monospace; font-size: 10px; text-transform: uppercase; padding: 0.35rem 0.75rem; border: 1px solid #333; color: #666; }
.chip.on { background: #39ff14; color: #000; border-color: #000; }
.tool { font-family: 'JetBrains Mono', monospace; font-size: 10px; padding: 0.35rem 0.5rem; border: 1px solid #333; color: #aaa; background: #111; min-height: 32px; }
.stat { border: 1px solid #333; padding: 0.75rem; }
.stat .lbl { color: #666; }
.stat .val { font-family: 'JetBrains Mono', monospace; font-size: 1.25rem; color: #39ff14; display: block; margin-top: 0.25rem; }
</style>
