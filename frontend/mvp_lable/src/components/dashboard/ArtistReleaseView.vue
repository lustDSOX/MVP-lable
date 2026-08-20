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
      <p class="font-mono text-[10px] text-[#ff0000] uppercase mb-1">Замечания</p>
      <p class="text-sm text-gray-200 whitespace-pre-wrap">{{ track.rejectReason }}</p>
    </div>
    <div v-if="track.status === 'changes_requested'" class="border-2 border-[#f97316] bg-[#1a0a00] p-4">
      <p class="font-mono text-[10px] text-[#f97316] uppercase mb-1">Требуются правки</p>
      <p class="text-sm text-gray-200 whitespace-pre-wrap">{{ track.changeRequestNote || track.rejectReason }}</p>
    </div>
    <div v-if="track.liveRevision && track.status === 'pending'" class="border-2 border-[#facc15] bg-[#1a1500] p-4">
      <p class="font-mono text-[10px] text-[#facc15] uppercase">LIVE_REVISION</p>
    </div>
    <div v-if="track.contract?.status === 'needs_resign'" class="border-2 border-[#facc15] bg-[#1a1500] p-4">
      <button type="button" class="btn-green" @click="resign">Переподписать договор</button>
    </div>
    <div class="flex flex-wrap gap-2 border-b border-[#333] pb-2">
      <button v-for="t in tabs" :key="t.id" type="button" class="tab" :class="{ on: tab === t.id }" @click="tab = t.id">{{ t.label }}</button>
    </div>
    <div v-if="tab === 'view'" class="space-y-4">
      <div class="grid sm:grid-cols-[160px_1fr] gap-4">
        <img v-if="track.coverUrl" :src="track.coverUrl" alt="cover" class="w-full aspect-square object-cover border-2 border-[#333]" />
        <div class="grid sm:grid-cols-2 gap-2 font-mono text-xs">
          <p><span class="text-gray-500">Жанры</span><br />{{ genreDisplay }}</p>
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
        <pre class="whitespace-pre-wrap font-mono text-sm text-gray-200 border border-[#333] p-4 bg-black min-h-[320px] max-h-[70vh] overflow-y-auto">{{ listenTrack.lyrics || '' }}</pre>
      </template>
    </div>
    <div v-else-if="tab === 'stats'" class="space-y-4">
      <div class="grid grid-cols-2 gap-3">
        <div class="stat"><span class="lbl">Total Plays</span><span class="val">{{ connectedTotalPlays.toLocaleString() }}</span></div>
        <div class="stat"><span class="lbl">Royalties</span><span class="val">${{ track.royalties || 0 }}</span></div>
      </div>
      <p class="font-mono text-xs text-[#39FF14] uppercase">Подключённые площадки</p>
      <div v-if="connectedPlatformStats.length" class="space-y-2">
        <div v-for="row in connectedPlatformStats" :key="row.id" class="border border-[#333] p-3 flex justify-between font-mono text-xs">
          <span class="uppercase text-gray-400">{{ row.label }}</span>
          <span>{{ row.plays.toLocaleString() }}</span>
        </div>
      </div>
      <p v-else class="font-mono text-xs text-gray-600">Нет подключённых площадок</p>
      <template v-if="track.type && track.type !== 'single'">
        <p class="font-mono text-xs text-[#39FF14] uppercase mt-2">По трекам</p>
        <div v-for="tr in track.tracksDetail || []" :key="tr.localId" class="border border-[#333] p-3 flex justify-between font-mono text-xs">
          <span>#{{ tr.order }} {{ tr.title }}</span>
          <span>{{ (tr.plays || 0).toLocaleString() }}</span>
        </div>
        <div class="border border-[#39FF14] p-3 flex justify-between font-mono text-xs">
          <span class="text-[#39FF14]">ИТОГО РЕЛИЗ</span>
          <span>{{ trackTracksTotal.toLocaleString() }}</span>
        </div>
      </template>
    </div>
    <div v-else-if="tab === 'history'" class="space-y-2">
      <article v-for="(h, i) in historySorted" :key="i" class="border border-[#333] p-3 font-mono text-xs">
        <div class="flex justify-between text-gray-500"><span>{{ formatAt(h.at) }}</span><span class="text-[#39FF14]">{{ h.kind || 'system' }} · {{ h.action }}</span></div>
        <p class="text-gray-300 mt-1">by {{ h.by }}</p>
        <p v-if="h.note" class="text-white mt-1 whitespace-pre-wrap">{{ h.note }}</p>
      </article>
    </div>
    <div v-else-if="tab === 'edit'" class="space-y-4">
      <label class="block"><span class="lbl">Название</span><input v-model="form.title" class="field" /></label>
      <div>
        <span class="lbl">Обложка</span>
        <DropZone label="Перетащите обложку" button-label="Выбрать файл" accept="image/*" @file="onCoverFile">
          <img v-if="form.coverUrl" :src="form.coverUrl" alt="cover" class="w-28 h-28 object-cover border-2 border-[#333] mx-auto" />
        </DropZone>
      </div>
      <div class="grid sm:grid-cols-2 gap-3">
        <label class="block"><span class="lbl">Тип</span>
          <select v-model="form.type" class="field">
            <option value="single">single</option><option value="ep">ep</option><option value="album">album</option>
          </select>
        </label>
        <label class="block">
          <span class="lbl">Дата релиза</span>
          <input v-model="form.releaseDate" type="date" class="field" :min="minDate" :disabled="dateLocked" :class="{ 'opacity-50 cursor-not-allowed': dateLocked }" />
          <span v-if="dateLocked" class="font-mono text-[9px] text-gray-500">Зафиксирована для published</span>
        </label>
      </div>
      <div>
        <span class="lbl">Жанры</span>
        <GenrePicker v-model="form.genres" />
      </div>
      <div v-for="(tr, idx) in form.tracks" :key="tr.localId" class="border border-[#333] p-4 space-y-3">
        <p class="font-mono text-xs text-[#39FF14] uppercase">Трек #{{ idx + 1 }}</p>
        <label class="block"><span class="lbl">Название</span><input v-model="tr.title" class="field" /></label>
        <label class="flex items-center gap-2 font-mono text-xs"><input type="checkbox" v-model="tr.isExplicit" class="accent-[#39FF14]" /> Explicit</label>
        <div>
          <span class="lbl">Аудио</span>
          <div class="mt-1 space-y-2">
            <AudioPlayer v-if="tr.audioUrl" :src="tr.audioUrl" :title="tr.title" />
            <DropZone label="Перетащите аудио" button-label="Выбрать файл" accept="audio/*" @file="(f) => onAudioFile(f, idx)" />
          </div>
        </div>
        <div>
          <span class="lbl">Текст</span>
          <div class="flex flex-wrap gap-1 mt-1 mb-2">
            <button type="button" class="tool" @click="insertVerse(idx)">Verse (авто #)</button>
            <button type="button" class="tool" @click="insertBlock(idx, 'Chorus')">Chorus</button>
            <button type="button" class="tool" @click="insertBlock(idx, 'Bridge')">Bridge</button>
            <button type="button" class="tool" @click="insertBlock(idx, 'Intro')">Intro</button>
            <button type="button" class="tool" @click="insertBlock(idx, 'Outro')">Outro</button>
          </div>
          <p class="font-mono text-[9px] text-gray-500 mb-1">[Verse 1: Name1, Name2]</p>
          <textarea v-model="tr.lyrics" rows="18" class="field font-mono text-sm" />
        </div>
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
import GenrePicker from '@/components/ui/GenrePicker.vue'
import DropZone from '@/components/ui/DropZone.vue'
import { usePlatformsStore } from '@/stores/platforms'

const props = defineProps<{ trackId: string }>()
defineEmits<{ close: [] }>()

const tracks = useTracksStore()
const auth = useAuthStore()
const notif = useNotificationsStore()
notif.hydrate()
const platformsStore = usePlatformsStore()
platformsStore.hydrate()
const tab = ref<'view' | 'listen' | 'stats' | 'history' | 'edit'>('view')
const listenId = ref<string | null>(null)
const saveMsg = ref('')
const minDate = new Date().toISOString().slice(0, 10)

const tabs = [
  { id: 'view' as const, label: 'Обзор' },
  { id: 'listen' as const, label: 'Слушать' },
  { id: 'stats' as const, label: 'Статистика' },
  { id: 'history' as const, label: 'История' },
  { id: 'edit' as const, label: 'Редактировать' },
]

const track = computed(() => tracks.tracks.find((t) => t.id === props.trackId) || null)
const dateLocked = computed(() => track.value?.status === 'published' && !track.value?.liveRevision)
const genreDisplay = computed(() => {
  const t = track.value as any
  if (!t) return '—'
  if (t.genres?.length) return t.genres.join(', ')
  return t.genre || '—'
})
const statusClass = computed(() => {
  const s = track.value?.status
  if (s === 'rejected') return 'border-[#ff0000] text-[#ff0000]'
  if (s === 'published') return 'border-[#39FF14] text-[#39FF14]'
  if (s === 'pending') return 'border-[#facc15] text-[#facc15]'
  if (s === 'changes_requested') return 'border-[#f97316] text-[#f97316]'
  return 'border-[#444] text-gray-400'
})
const historySorted = computed(() => [...(track.value?.moderationLog || [])].reverse())
const connectedPlatformStats = computed(() => {
  const plat = track.value?.platforms
  if (!plat) return [] as { id: string; label: string; plays: number }[]
  const keyMap: Record<string, 'spotify' | 'apple' | 'yandex' | 'vk'> = {
    spotify: 'spotify', apple: 'apple', yandex: 'yandex', vk: 'vk',
  }
  return platformsStore.accounts
    .filter((a) => a.connected)
    .map((a) => {
      const k = keyMap[a.id]
      return { id: a.id, label: a.label, plays: k ? Number(plat[k] ?? 0) : 0 }
    })
})
const connectedTotalPlays = computed(() => connectedPlatformStats.value.reduce((s, r) => s + r.plays, 0))
const trackTracksTotal = computed(() => {
  const list = track.value?.tracksDetail || []
  const sum = list.reduce((s, tr) => s + (tr.plays || 0), 0)
  return sum || connectedTotalPlays.value
})
const listenTrack = computed(() => track.value?.tracksDetail?.find((t) => t.localId === listenId.value) || track.value?.tracksDetail?.[0] || null)

const form = reactive({
  title: '',
  type: 'single' as string,
  genres: [] as string[],
  releaseDate: '',
  coverUrl: '' as string | undefined,
  tracks: [] as NonNullable<Track['tracksDetail']>,
})

function syncForm() {
  const t = track.value as any
  if (!t) return
  form.title = t.title
  form.type = t.type || 'single'
  form.genres = t.genres?.length ? [...t.genres] : t.genre ? String(t.genre).split(/[,/]/).map((s: string) => s.trim()).filter(Boolean) : []
  form.releaseDate = t.releaseDate || ''
  form.coverUrl = t.coverUrl
  form.tracks = JSON.parse(JSON.stringify(t.tracksDetail || []))
  if (!listenId.value && form.tracks[0]) listenId.value = form.tracks[0].localId
}
watch(track, syncForm, { immediate: true })

function onCoverFile(f: File) {
  form.coverUrl = URL.createObjectURL(f)
}
function onAudioFile(f: File, idx: number) {
  if (!form.tracks[idx]) return
  form.tracks[idx].audioUrl = URL.createObjectURL(f)
  form.tracks[idx].masterFile = f.name
}
function nextVerseNum(lyrics: string) {
  const matches = lyrics.match(/\[Verse\s+(\d+)/gi) || []
  let max = 0
  for (const m of matches) {
    const n = parseInt(m.replace(/\D/g, ''), 10)
    if (n > max) max = n
  }
  return max + 1
}
function insertVerse(idx: number) {
  const tr = form.tracks[idx]
  if (!tr) return
  const n = nextVerseNum(tr.lyrics || '')
  const artist = track.value?.artistName || 'Artist'
  tr.lyrics = `${tr.lyrics || ''}\n[Verse ${n}: ${artist}]\n`
}
function insertBlock(idx: number, kind: string) {
  const tr = form.tracks[idx]
  if (!tr) return
  const artist = track.value?.artistName || 'Artist'
  tr.lyrics = `${tr.lyrics || ''}\n[${kind}: ${artist}]\n`
}

function save() {
  if (!track.value) return
  const patch: any = {
    title: form.title,
    type: form.type,
    genre: form.genres.join(', '),
    genres: form.genres,
    coverUrl: form.coverUrl,
    tracksDetail: form.tracks,
  }
  if (!dateLocked.value) {
    if (form.releaseDate && form.releaseDate < minDate) {
      saveMsg.value = 'Дата релиза не может быть раньше сегодня'
      return
    }
    patch.releaseDate = form.releaseDate
  }
  const { needsResign } = tracks.updateRelease(track.value.id, patch, auth.email || 'artist')
  if (needsResign) { saveMsg.value = 'Сохранено. Нужен re-sign.'; tab.value = 'view' }
  else if (track.value?.liveRevision || track.value?.status === 'pending') saveMsg.value = 'Сохранено. На проверке.'
  else saveMsg.value = 'Сохранено.'
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
    notif.notifyUser(e, live ? 'LIVE revision' : 'Новый релиз', `«${track.value.title}»`, 'release_pending')
  }
  saveMsg.value = 'Отправлено.'
  tab.value = 'history'
}

function resign() {
  if (!track.value) return
  tracks.resignContract(track.value.id, auth.artistName || 'Artist', auth.email || 'artist')
  saveMsg.value = 'Договор переподписан.'
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
