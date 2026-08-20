<template>
  <div class="min-h-screen pt-24 px-4 pb-12 font-['Inter',sans-serif] text-white relative">
    <div class="max-w-7xl mx-auto flex flex-col gap-12 relative z-10">
      <section class="command-center-grid">
        <div class="welcome-block">
          <h1 class="font-planet h1-metal-textured" :data-text="authStore.artistName || 'UNKNOWN'">{{ authStore.artistName || 'UNKNOWN' }}</h1>
          <span class="welcome-subtitle">Artist_Terminal</span>
        </div>
        <div class="search-wrapper">
          <input type="text" v-model="searchQuery" placeholder="Search release by title..." class="search-input" />
        </div>
        <button @click="isContractModalOpen = true" class="upload-button group">
          <span class="relative z-10 text-2xl">Upload New Release</span>
        </button>
      </section>

      <section class="data-panel-container">
        <div class="platform-tabs">
          <button
            v-for="platform in platformTabs"
            :key="platform"
            @click="activePlatform = platform"
            :class="['platform-tab', { active: platform === activePlatform }]"
          >{{ platform }}</button>
        </div>
        <div class="data-panel-content">
          <div class="stat-item"><span class="label">Total Plays</span><span class="value">{{ displayedPlays.toLocaleString() }}</span></div>
          <div class="stat-item"><span class="label">Total Releases</span><span class="value">{{ tracksStore.tracks.length }}</span></div>
          <div class="stat-item"><span class="label">Platform Share</span><span class="value">{{ platformShare }}%</span></div>
        </div>
      </section>

      <div class="flex flex-wrap gap-2 mb-2">
        <button type="button" class="cab-tab" :class="{ on: cabinetTab === 'releases' }" @click="cabinetTab = 'releases'; selectedReleaseId = null">Релизы</button>
        <button type="button" class="cab-tab" :class="{ on: cabinetTab === 'platforms' }" @click="cabinetTab = 'platforms'; selectedReleaseId = null">Площадки</button>
      </div>

      <PlatformsPanel v-if="cabinetTab === 'platforms'" />

      <ArtistReleaseView
        v-if="cabinetTab === 'releases' && selectedReleaseId"
        :track-id="selectedReleaseId"
        @close="selectedReleaseId = null"
      />

      <section v-if="cabinetTab === 'releases' && !selectedReleaseId" class="bg-black border border-[#333]">
        <div class="md:hidden space-y-3 p-3">
          <article v-for="track in filteredTracks" :key="'m-'+track.id" class="border-2 border-[#333] bg-[#0a0a0a] p-4 flex flex-col gap-2 cursor-pointer hover:border-[#39FF14]" @click="openRelease(track.id)">
            <div class="flex justify-between gap-2"><h3 class="font-bold text-white uppercase text-sm">{{ track.title }}</h3><span class="text-[10px] font-mono uppercase border border-[#444] px-2">{{ track.status }}</span></div>
            <p class="text-xs text-gray-500 font-mono">Plays: {{ track.plays ?? 0 }}</p>
            <button v-if="track.status === 'draft'" type="button" @click.stop="continueDraft(track.id)" class="action-button draft-button min-h-[44px] w-full">[CONTINUE]</button>
          </article>
        </div>
        <div class="overflow-x-auto hidden md:block">
          <table class="w-full text-left min-w-[600px]">
            <thead class="table-header"><tr><th class="table-th">Title</th><th class="table-th text-center">Status</th><th class="table-th text-right">Plays</th></tr></thead>
            <tbody>
              <tr v-if="tracksStore.isLoading"><td colspan="3" class="p-8 text-center text-[#ff0000] font-mono">LOADING...</td></tr>
              <tr v-for="track in filteredTracks" :key="track.id" class="table-row row-clickable" @click="openRelease(track.id)">
                <td class="p-4"><h3 class="track-title">{{ track.title }}</h3>
                  <div v-if="track.status === 'rejected'" class="rejection-reason">REASON: {{ track.rejectReason }}</div></td>
                <td class="p-4 text-center">
                  <span v-if="track.status === 'published'" class="status-badge status-online">ONLINE</span>
                  <span v-else-if="track.status === 'pending'" class="status-badge status-scanning">SCANNING</span>
                  <span v-else-if="track.status === 'rejected'" class="status-badge status-error">ERROR</span>
                  <span v-else-if="track.status === 'changes_requested'" class="status-badge status-error">CHANGES</span>
                  <span v-else class="status-badge status-draft">{{ track.status }}</span>
                </td>
                <td class="p-4 text-right font-mono text-xl">{{ track.plays.toLocaleString() }}</td>
              </tr>
            </tbody>
          </table>
        </div>
      </section>
    </div>

    <ContractModal :is-open="isContractModalOpen" @close="isContractModalOpen = false" @success="handleContractSuccess" />
    <div v-if="activeDraftId"><TrackUploadForm :track-id="activeDraftId" @track-uploaded="onTrackUploaded" /></div>
  </div>
</template>

<style scoped>
.command-center-grid { display: grid; grid-template-columns: 1fr 380px; gap: 2rem; align-items: end; }
.welcome-block { grid-column: 1 / -1; margin-bottom: 1rem; }
.search-input { width: 100%; background: #000; border: 2px solid #333; padding: 1.25rem; font-family: 'JetBrains Mono', monospace; color: #fff; text-transform: uppercase; }
.upload-button { width: 100%; padding: 1rem; background: #fff; color: #000; border: 4px solid #000; text-transform: uppercase; box-shadow: 4px 4px 0 #ff0000; font-family: 'Archivo Black', sans-serif; }
.welcome-subtitle { font-family: 'JetBrains Mono', monospace; font-size: 10px; color: #6b7280; text-transform: uppercase; letter-spacing: 0.4em; display: block; margin-top: 0.5rem; }
.data-panel-container { border: 2px solid #333; background: #000; }
.platform-tabs { display: flex; border-bottom: 2px solid #333; overflow-x: auto; }
.platform-tab { padding: 0.75rem 1.5rem; font-family: 'JetBrains Mono', monospace; text-transform: uppercase; font-size: 0.875rem; color: #6b7280; border-right: 2px solid #333; background: transparent; }
.platform-tab.active { background: #ff0000; color: #fff; }
.data-panel-content { display: grid; grid-template-columns: repeat(3, 1fr); gap: 1px; background: #333; }
.stat-item { background: #000; padding: 1.5rem; display: flex; flex-direction: column; }
.stat-item .label { font-family: 'JetBrains Mono', monospace; font-size: 0.875rem; color: #6b7280; text-transform: uppercase; margin-bottom: 0.75rem; }
.stat-item .value { font-family: 'Archivo Black', sans-serif; font-size: 3rem; line-height: 1; }
.table-header { border-bottom: 2px solid #333; }
.table-th { padding: 1rem; text-transform: uppercase; font-family: 'JetBrains Mono', monospace; font-size: 0.875rem; color: #6b7280; }
.table-row { border-bottom: 1px solid #222; }
.row-clickable { cursor: pointer; transition: background 0.15s; }
.row-clickable:hover { background: #111; }
.row-clickable:hover .track-title { color: #39FF14; }
.track-title { font-family: 'Archivo Black', sans-serif; font-size: 1.25rem; text-transform: uppercase; }
.rejection-reason { margin-top: 0.5rem; padding-left: 0.75rem; border-left: 2px solid #ff0000; font-family: 'JetBrains Mono', monospace; font-size: 0.75rem; color: #ff0000; }
.status-badge { font-family: 'JetBrains Mono', monospace; font-weight: 700; font-size: 0.75rem; padding: 0.25rem 0.5rem; text-transform: uppercase; }
.status-online { background: #39FF14; color: #000; }
.status-scanning { background: #2563eb; color: #fff; }
.status-error { background: #ff0000; color: #fff; }
.status-draft { background: #f59e0b; color: #000; }
.action-button { background: #222; color: #9ca3af; padding: 0.5rem; border: none; cursor: pointer; }
.action-button.draft-button { background: #39FF14; color: #000; font-family: 'JetBrains Mono', monospace; font-size: 0.75rem; padding: 0.5rem 0.75rem; }
.cab-tab { font-family: 'JetBrains Mono', monospace; font-size: 11px; text-transform: uppercase; padding: 0.5rem 1rem; min-height: 44px; border: 2px solid #333; color: #888; background: #0a0a0a; }
.cab-tab.on { background: #39FF14; color: #000; border-color: #000; font-weight: 700; }
@media (max-width: 1024px) { .command-center-grid { grid-template-columns: 1fr; } }
@media (max-width: 768px) { .data-panel-content { grid-template-columns: 1fr; } .stat-item .value { font-size: 2rem; } }
</style>

<script lang="ts" setup>
import { ref, computed, onMounted } from 'vue'
import { useAuthStore } from '@/stores/auth'
import { useTracksStore } from '@/stores/tracks'
import { usePlatformsStore } from '@/stores/platforms'
import ContractModal from '@/components/track/ContractModal.vue'
import TrackUploadForm from '@/components/track/TrackUploadForm.vue'
import PlatformsPanel from '@/components/dashboard/PlatformsPanel.vue'
import ArtistReleaseView from '@/components/dashboard/ArtistReleaseView.vue'

const authStore = useAuthStore()
const tracksStore = useTracksStore()
const platformsStore = usePlatformsStore()
platformsStore.hydrate()

const isContractModalOpen = ref(false)
const cabinetTab = ref<'releases' | 'platforms'>('releases')
const selectedReleaseId = ref<string | null>(null)
const activeDraftId = ref<string | null>(null)
const searchQuery = ref('')
const activePlatform = ref('Total')

const platformTabs = computed(() => {
  const connected = platformsStore.accounts.filter((a) => a.connected)
  const labels: Record<string, string> = { yandex: 'ЯМ', vk: 'VK', apple: 'Apple', spotify: 'Spotify' }
  return ['Total', ...connected.map((a) => labels[a.id] || a.label)]
})

const displayedPlays = computed(() => {
  if (activePlatform.value === 'Total') return tracksStore.totalPlays
  const map: Record<string, 'spotify' | 'apple' | 'yandex' | 'vk'> = { Spotify: 'spotify', Apple: 'apple', 'ЯМ': 'yandex', VK: 'vk' }
  const key = map[activePlatform.value]
  if (!key) return tracksStore.totalPlays
  return tracksStore.tracks.reduce((s, tr) => s + (tr.platforms?.[key] ?? 0), 0)
})

const platformShare = computed(() => {
  if (activePlatform.value === 'Total' || tracksStore.totalPlays === 0) return 100
  return Math.round((displayedPlays.value / tracksStore.totalPlays) * 100)
})

const filteredTracks = computed(() => {
  if (!searchQuery.value.trim()) return tracksStore.tracks
  const q = searchQuery.value.toLowerCase()
  return tracksStore.tracks.filter((t) => t.title.toLowerCase().includes(q))
})

const handleContractSuccess = (payload: { release?: { title: string; type?: string; tracks?: unknown[] }; trackTitle?: string }) => {
  isContractModalOpen.value = false
  const rel = payload?.release
  const title = rel?.title || payload?.trackTitle || 'Новый релиз'
  activeDraftId.value = tracksStore.createFromRelease({ title, type: rel?.type, trackCount: rel?.tracks?.length ?? 1 })
}
const continueDraft = (id: string) => { activeDraftId.value = id }
const onTrackUploaded = (id: string) => { tracksStore.completeTrackUpload(id); activeDraftId.value = null }

function openRelease(id: string) {
  selectedReleaseId.value = id
  cabinetTab.value = 'releases'
}

onMounted(() => tracksStore.fetchTracks())
</script>
