<template>
  <form @submit.prevent="onSubmit" class="contract-form font-['Inter',sans-serif]">
    <div class="form-section">
      <div class="section-header">
        <h4 class="section-title">01 // ARTIST_PROFILE</h4>
        <div class="section-line"></div>
      </div>
      <p class="hint">Данные из аккаунта. Правка — в профиле.</p>
      <div class="grid grid-cols-1 md:grid-cols-2 gap-x-8 gap-y-4">
        <div class="input-group">
          <label class="input-label"><span>FULL_LEGAL_NAME</span></label>
          <input :value="profile.fullName" type="text" readonly class="form-input readonly" />
        </div>
        <div class="input-group">
          <label class="input-label"><span>UPLINK_MAIL</span></label>
          <input :value="profile.email" type="email" readonly class="form-input readonly" />
        </div>
        <div class="input-group">
          <label class="input-label"><span>ARTIST_ALIAS</span></label>
          <input :value="profile.artistName" type="text" readonly class="form-input readonly" />
        </div>
        <div class="input-group">
          <label class="input-label"><span>COMM_PHONE</span></label>
          <input v-model="profile.phone" type="tel" placeholder="+7…" class="form-input" />
        </div>
        <div class="input-group md:col-span-2">
          <label class="input-label"><span>NETWORK_CREDENTIALS</span></label>
          <input v-model="profile.socialNetworks" type="text" placeholder="VK / TG / IG" class="form-input" />
        </div>
        <div class="input-group">
          <label class="input-label"><span>SUBJECT_AGE</span></label>
          <input v-model.number="profile.age" type="number" min="14" max="100" class="form-input" />
        </div>
        <div class="input-group">
          <label class="input-label"><span>LOCATION_ZONE</span></label>
          <input v-model="profile.city" type="text" placeholder="MOSCOW" class="form-input" />
        </div>
      </div>
    </div>

    <div class="form-section">
      <div class="section-header">
        <h4 class="section-title text-red">02 // RELEASE</h4>
        <div class="section-line bg-red"></div>
      </div>
      <div class="grid grid-cols-1 md:grid-cols-2 gap-x-8 gap-y-4">
        <div class="input-group">
          <label class="input-label"><span>RELEASE_TYPE</span><span class="required-mark">*REQ</span></label>
          <select v-model="releaseType" class="form-input" required>
            <option value="single">Single (1 track)</option>
            <option value="ep">EP (2–6 tracks)</option>
            <option value="album">Album (7+ tracks)</option>
          </select>
        </div>
        <div class="input-group">
          <label class="input-label"><span>RELEASE_TITLE</span><span class="required-mark">*REQ</span></label>
          <input v-model="releaseTitle" type="text" required placeholder="ALBUM / SINGLE NAME" class="form-input border-red" />
        </div>
        <div class="input-group">
          <label class="input-label"><span>RELEASE_DATE</span></label>
          <input v-model="releaseDate" type="date" class="form-input" :min="minDate" @change="clampDate" />
        </div>
      </div>
      <p class="hint">Один договор на весь релиз. Треклист — спецификация к договору.</p>
    </div>

    <div class="form-section">
      <div class="section-header">
        <h4 class="section-title">03 // TRACKLIST</h4>
        <div class="section-line"></div>
      </div>
      <p class="hint">Для EP/альбома — каждый трек отдельно. Фиты и роли — на треке.</p>

      <div v-for="(track, idx) in tracks" :key="track.localId" class="track-card">
        <div class="track-card-head">
          <span class="font-mono text-xs text-[#39FF14]">TRACK {{ idx + 1 }}</span>
          <button v-if="tracks.length > 1" type="button" class="text-[#ff0000] font-mono text-[10px] uppercase" @click="removeTrack(idx)">Remove</button>
        </div>
        <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
          <div class="input-group md:col-span-2">
            <label class="input-label"><span>TITLE</span><span class="required-mark">*REQ</span></label>
            <input v-model="track.title" type="text" required class="form-input" placeholder="TRACK_NAME" />
          </div>
          <label class="flex items-center gap-2 font-mono text-xs uppercase text-gray-400">
            <input v-model="track.isExplicit" type="checkbox" class="accent-[#39FF14]" /> Explicit
          </label>
        </div>
        <div class="mt-3">
          <p class="input-label mb-2"><span>GENRES (трек)</span></p>
          <GenrePicker v-model="track.genres" />
        </div>
        <div class="mt-3">
          <p class="input-label mb-2"><span>CONTRIBUTORS</span></p>
          <div v-for="(c, cIdx) in track.contributors" :key="cIdx" class="space-y-2 mb-3 border border-[#222] p-3">
            <select v-model="c.role" class="form-input w-full">
              <option value="main_artist">Main artist</option>
              <option value="featured">Featured</option>
              <option value="producer">Producer</option>
              <option value="songwriter">Songwriter</option>
              <option value="other">Other</option>
            </select>
            <label class="block">
              <span class="font-mono text-[9px] text-gray-500 uppercase">Имя контрибьютора</span>
              <input v-model="c.creditName" type="text" class="form-input w-full mt-1" placeholder="Name / alias" />
            </label>
            <button type="button" class="font-mono text-[10px] text-gray-500 uppercase min-h-[40px]" @click="track.contributors.splice(cIdx, 1)">Удалить</button>
          </div>
          <button type="button" class="add-btn" @click="addContributor(track)">+ contributor</button>
        </div>
      </div>

      <button v-if="releaseType !== 'single' || tracks.length < 1" type="button" class="add-btn mt-2" :disabled="releaseType === 'single' && tracks.length >= 1" @click="addTrack">+ add track</button>
    </div>

    <button type="submit" :disabled="isLoading || !canSubmit" class="submit-button">
      <span v-if="!isLoading">>>> GENERATE_RELEASE_CONTRACT</span>
      <span v-else>PROCESSING…</span>
    </button>
  </form>
</template>

<script setup lang="ts">
import { ref, computed, watch, onMounted } from 'vue'
import { useAuthStore } from '@/stores/auth'
import GenrePicker from '@/components/ui/GenrePicker.vue'
import type { ReleaseDraft, ReleaseType, TrackInput, ContributorInput, ArtistProfileSnapshot } from '@/types/release'

defineProps<{ isLoading?: boolean }>()
const emit = defineEmits<{ 'submit-form': [payload: ReleaseDraft] }>()
const auth = useAuthStore()

const profile = ref<ArtistProfileSnapshot>({
  fullName: '', email: '', phone: '', artistName: '', socialNetworks: '', age: null, city: '',
})
const releaseType = ref<ReleaseType>('single')
const releaseTitle = ref('')
const minDate = new Date().toISOString().slice(0, 10)
const releaseDate = ref(new Date().toISOString().slice(0, 10))
const tracks = ref<TrackInput[]>([])

function newTrack(order: number): TrackInput {
  return {
    localId: `t-${Date.now()}-${order}`,
    title: '',
    order,
    isExplicit: false,
    lyrics: '',
    genres: [] as string[],
    contributors: [{ role: 'main_artist', creditName: auth.artistName || profile.value.artistName || '' }],
  }
}
function addTrack() {
  if (releaseType.value === 'single' && tracks.value.length >= 1) return
  tracks.value.push(newTrack(tracks.value.length + 1))
}
function removeTrack(idx: number) {
  tracks.value.splice(idx, 1)
  tracks.value.forEach((t, i) => { t.order = i + 1 })
}
function addContributor(track: TrackInput) {
  track.contributors.push({ role: 'featured', creditName: '' } as ContributorInput)
}
watch(releaseType, (t) => {
  if (t === 'single' && tracks.value.length > 1) tracks.value = tracks.value[0] ? [tracks.value[0]] : []
  if (tracks.value.length === 0) addTrack()
})
onMounted(() => {
  profile.value = {
    fullName: auth.artistName || '—',
    email: auth.email || '',
    phone: '',
    artistName: auth.artistName || '',
    socialNetworks: '',
    age: null,
    city: '',
  }
  if (!tracks.value.length) addTrack()
})
function clampDate() {
  if (releaseDate.value && releaseDate.value < minDate) releaseDate.value = minDate
}
const canSubmit = computed(() => {
  if (!releaseTitle.value.trim() || !tracks.value.length) return false
  return tracks.value.every((t) => t.title.trim())
})
function onSubmit() {
  if (!canSubmit.value) return
  emit('submit-form', {
    type: releaseType.value,
    title: releaseTitle.value.trim(),
    genre: [...new Set(tracks.value.flatMap((tr) => tr.genres || []))].join(', '),
    genres: [...new Set(tracks.value.flatMap((tr) => tr.genres || []))],
    releaseDate: releaseDate.value || new Date().toISOString().slice(0, 10),
    contractRequired: true,
    profile: { ...profile.value },
    tracks: tracks.value.map((t, i) => ({
      ...t,
      order: i + 1,
      title: t.title.trim(),
      contributors: t.contributors.filter((c) => c.creditName.trim()),
    })),
  })
}
</script>

<style scoped>
.contract-form { display: flex; flex-direction: column; gap: 2.5rem; position: relative; z-index: 10; }
.hint { font-family: 'JetBrains Mono', monospace; font-size: 0.65rem; color: #6b7280; text-transform: uppercase; margin: 0 0 0.5rem; }
.form-section { display: flex; flex-direction: column; gap: 1rem; }
.section-header { display: flex; align-items: center; gap: 1rem; }
.section-title { font-family: 'Archivo Black', sans-serif; font-size: 1.25rem; color: white; text-transform: uppercase; margin: 0; }
.section-title.text-red { color: #ff0000; }
.section-line { flex: 1; height: 2px; background: #333; }
.section-line.bg-red { background: #ff0000; opacity: 0.5; }
.input-group { display: flex; flex-direction: column; gap: 0.4rem; }
.input-label { display: flex; justify-content: space-between; font-family: 'JetBrains Mono', monospace; font-size: 0.625rem; color: #9ca3af; text-transform: uppercase; letter-spacing: 0.1em; }
.required-mark { color: #ff0000; }
.form-input { width: 100%; padding: 0.75rem 1rem; background: #000; border: 2px solid #333; color: #fff; font-family: 'JetBrains Mono', monospace; font-size: 0.9rem; text-transform: uppercase; min-height: 44px; }
.form-input.readonly { opacity: 0.7; border-color: #222; cursor: default; }
.form-input:focus { outline: none; border-color: #fff; }
.form-input.border-red:focus { border-color: #ff0000; }
.track-card { border: 2px solid #333; padding: 1rem; background: #050505; margin-bottom: 0.75rem; }
.track-card-head { display: flex; justify-content: space-between; margin-bottom: 0.75rem; }
.add-btn { font-family: 'JetBrains Mono', monospace; font-size: 0.7rem; text-transform: uppercase; color: #39ff14; border: 1px dashed #39ff14; padding: 0.5rem 0.75rem; background: transparent; min-height: 44px; }
.submit-button { width: 100%; padding: 1.25rem; background: #fff; color: #000; border: 4px solid #000; text-transform: uppercase; font-family: 'Archivo Black', sans-serif; font-size: 1.1rem; box-shadow: 6px 6px 0 #ff0000; min-height: 52px; }
.submit-button:disabled { opacity: 0.5; cursor: not-allowed; }
</style>
