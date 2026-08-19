<template>
  <div class="min-h-screen pt-24 px-4 pb-12 font-['Inter',sans-serif] text-white relative">
    <div class="max-w-7xl mx-auto flex flex-col gap-12 relative z-10">
      
      <section class="command-center-grid">
        <div class="welcome-block">
          <h1 class="font-planet h1-metal-textured" :data-text="authStore.artistName || 'UNKNOWN'">
            {{ authStore.artistName || 'UNKNOWN' }}
          </h1>
          <span class="welcome-subtitle">Artist_Terminal</span>
        </div>

        <div class="search-wrapper">
          <input 
            type="text" 
            v-model="searchQuery"
            placeholder="Search release by title..."
            class="search-input"
          />
        </div>

        <button @click="isContractModalOpen = true" class="upload-button group">
          <span class="relative z-10 text-2xl">Upload New Release</span>
          <div class="absolute inset-0 crt-noise opacity-30"></div>
        </button>
      </section>

      <section class="data-panel-container">
        <div class="platform-tabs">
          <button
            v-for="platform in platforms"
            :key="platform"
            @click="activePlatform = platform"
            :class="['platform-tab', { 'active': platform === activePlatform }]"
          >
            {{ platform }}
          </button>
        </div>
        <div class="data-panel-content">
          <div class="stat-item">
            <span class="label">Total Plays</span>
            <span class="value">{{ displayedPlays.toLocaleString() }}</span>
          </div>
          <div class="stat-item">
            <span class="label">Total Releases</span>
            <span class="value">{{ tracksStore.tracks.length }}</span>
          </div>
          <div class="stat-item">
            <span class="label">Platform Share</span>
            <span class="value">{{ platformShare }}%</span>
          </div>
        </div>
      </section>

      <PlatformsPanel />

      <section class="bg-black border border-[#333]">
        <div class="md:hidden space-y-3 p-3 mobile-track-cards">
          <article
            v-for="track in filteredTracks"
            :key="'m-' + track.id"
            class="border-2 border-[#333] bg-[#0a0a0a] p-4 flex flex-col gap-2"
          >
            <div class="flex justify-between gap-2 items-start">
              <h3 class="font-bold text-white uppercase text-sm leading-tight">{{ track.title }}</h3>
              <span class="text-[10px] font-mono uppercase shrink-0 border border-[#444] px-2 py-0.5">{{ track.status }}</span>
            </div>
            <p class="text-xs text-gray-500 font-mono">Plays: {{ track.plays ?? 0 }}</p>
            <button
              v-if="track.status === 'draft'"
              type="button"
              @click="continueDraft(track.id)"
              class="action-button draft-button min-h-[44px] w-full"
            >[CONTINUE]</button>
          </article>
          <p v-if="!filteredTracks.length" class="text-center text-gray-600 py-8 font-mono text-sm">NO_RELEASES</p>
        </div>

        <div class="overflow-x-auto hidden md:block">
          <table class="w-full text-left min-w-[700px]">
            <thead class="table-header">
              <tr>
                <th class="table-th w-2/5">Title</th>
                <th class="table-th text-center">Status</th>
                <th class="table-th text-right">Plays</th>
                <th class="table-th text-center">Actions</th>
              </tr>
            </thead>
            <tbody>
              <tr v-if="tracksStore.isLoading">
                <td colspan="4" class="p-8 text-center text-[#ff0000] font-mono animate-pulse">LOADING DATA...</td>
              </tr>
              <tr v-else-if="filteredTracks.length === 0">
                <td colspan="4" class="p-8 text-center text-gray-600 font-mono">NO RELEASES FOUND.</td>
              </tr>
              <tr v-for="track in filteredTracks" :key="track.id" class="table-row">
                <td class="p-4 flex items-center gap-4">
                   <img :src="'/placeholder-cover.png'" class="w-12 h-12 object-cover bg-[#111]" alt="Cover">
                   <div>
                      <h3 class="track-title">{{ track.title }}</h3>
                      <div v-if="track.status === 'rejected'" class="rejection-reason">
                         REASON: {{ track.rejectReason }}
                      </div>
                   </div>
                </td>
                <td class="p-4 text-center">
                  <span v-if="track.status === 'published'" class="status-badge status-online">ONLINE</span>
                  <span v-else-if="track.status === 'pending'" class="status-badge status-scanning animate-pulse">SCANNING</span>
                  <span v-else-if="track.status === 'rejected'" class="status-badge status-error">ERROR</span>
                  <span v-else-if="track.status === 'draft'" class="status-badge status-draft">DRAFT</span>
                </td>
                <td class="p-4 text-right font-mono text-xl">{{ track.plays.toLocaleString() }}</td>
                <td class="p-4">
                  <div v-if="track.status === 'draft'" class="flex items-center justify-center">
                    <button @click="continueDraft(track.id)" class="action-button draft-button">[CONTINUE]</button>
                  </div>
                  <div v-else class="flex items-center justify-center gap-2">
                    <button class="action-button" title="Edit Release">✎</button>
                    <button class="action-button" title="Stats">◉</button>
                  </div>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </section>
    </div>

    <ContractModal 
      :is-open="isContractModalOpen" 
      @close="isContractModalOpen = false"
      @success="handleContractSuccess"
    />
    <div v-if="activeDraftId">
      <TrackUploadForm 
        :track-id="activeDraftId" 
        @track-uploaded="onTrackUploaded" 
      />
    </div>
  </div>
</template>

<style scoped>
.command-center-grid {
  display: grid;
  grid-template-columns: 1fr 380px; 
  gap: 2rem;
  align-items: end; 
}
.welcome-block {
  grid-column: 1 / -1; 
  width: 100%;
  align-self: start;
  margin-bottom: 1rem;
}
.search-wrapper { position: relative; width: 100%; }
.upload-button {
  width: 100%;
  padding: 1rem;
  background-color: white;
  color: black;
  border: 4px solid black;
  text-transform: uppercase;
  box-shadow: 4px 4px 0 #ff0000;
  font-family: 'Archivo Black', sans-serif;
  transition: all 0.15s;
  position: relative;
  overflow: hidden;
  height: fit-content; 
}
.upload-button:hover{ box-shadow: none; transform: translate(2px, 2px); }
@media (max-width: 1024px) {
  .command-center-grid { grid-template-columns: 1fr; gap: 1.5rem; }
  .welcome-block { margin-bottom: 0; }
  .upload-button { width: 100%; order: 3; }
}
.welcome-subtitle {
  font-family: 'JetBrains Mono', monospace;
  font-size: 10px;
  color: #6b7280;
  text-transform: uppercase;
  letter-spacing: 0.4em;
  margin-top: 0.5rem;
  display: block;
}
.search-input {
  width: 100%;
  background-color: black;
  border: 2px solid #333;
  padding: 1.25rem 1.5rem;
  font-family: 'JetBrains Mono', monospace;
  font-size: 1.125rem;
  color: white;
  text-transform: uppercase;
}
.search-input:focus { outline: none; border-color: #ff0000; }
.data-panel-container { border: 2px solid #333; background-color: black; }
.platform-tabs { display: flex; border-bottom: 2px solid #333; overflow-x: auto; }
.platform-tab {
  padding: 0.75rem 1.5rem;
  font-family: 'JetBrains Mono', monospace;
  text-transform: uppercase;
  font-size: 0.875rem;
  color: #6b7280;
  border-right: 2px solid #333;
  background-color: transparent;
  white-space: nowrap;
}
.platform-tab:last-child { border-right: none; }
.platform-tab.active { background-color: #ff0000; color: white; }
.data-panel-content {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 1px;
  background-color: #333;
}
.stat-item {
  background-color: black;
  padding: 1.5rem;
  display: flex;
  flex-direction: column;
}
.stat-item .label {
  font-family: 'JetBrains Mono', monospace;
  font-size: 0.875rem;
  color: #6b7280;
  text-transform: uppercase;
  letter-spacing: 0.1em;
  margin-bottom: 0.75rem;
}
.stat-item .value {
  font-family: 'Archivo Black', sans-serif;
  font-size: 3rem;
  line-height: 1;
  letter-spacing: -0.05em;
}
.table-header { border-bottom: 2px solid #333; }
.table-th {
  padding: 1rem;
  text-transform: uppercase;
  letter-spacing: 0.1em;
  font-family: 'JetBrains Mono', monospace;
  font-size: 0.875rem;
  color: #6b7280;
}
.table-row { border-bottom: 1px solid #222; }
.table-row:hover { background-color: #0a0a0a; }
.track-title {
  font-family: 'Archivo Black', sans-serif;
  font-size: 1.25rem;
  text-transform: uppercase;
}
.rejection-reason {
  margin-top: 0.5rem;
  padding-left: 0.75rem;
  border-left: 2px solid #ff0000;
  font-family: 'JetBrains Mono', monospace;
  font-size: 0.75rem;
  color: #ff0000;
  text-transform: uppercase;
}
.status-badge {
  font-family: 'JetBrains Mono', monospace;
  font-weight: 700;
  font-size: 0.75rem;
  padding: 0.25rem 0.5rem;
  text-transform: uppercase;
}
.status-online { background-color: #39FF14; color: black; }
.status-scanning { background-color: #2563eb; color: white; }
.status-error { background-color: #ff0000; color: white; }
.status-draft { background-color: #f59e0b; color: black; }
.action-button {
  background-color: #222;
  color: #9ca3af;
  padding: 0.5rem;
}
.action-button:hover { background-color: #ff0000; color: black; }
.action-button.draft-button {
  background-color: #39FF14;
  color: black;
  font-family: 'JetBrains Mono', monospace;
  font-size: 0.75rem;
  padding: 0.5rem 0.75rem;
}
@media (max-width: 768px) {
  .data-panel-content { grid-template-columns: 1fr; }
  .stat-item .value { font-size: 2rem; }
}
.crt-noise {
  background-image: url('data:image/svg+xml;utf8,%3Csvg viewBox="0 0 200 200" xmlns="http://www.w3.org/2000/svg"%3E%3Cfilter id="noiseFilter"%3E%3CfeTurbulence type="fractalNoise" baseFrequency="0.9" numOctaves="3" stitchTiles="stitch"/%3E%3C/filter%3E%3Crect width="100%25" height="100%25" filter="url(%23noiseFilter)"/%3E%3C/svg%3E');
}
</style>

<script lang="ts" setup>
import { ref, computed, onMounted } from 'vue'
import { useAuthStore } from '@/stores/auth'
import { useTracksStore } from '@/stores/tracks'

import ContractModal from '@/components/track/ContractModal.vue'
import TrackUploadForm from '@/components/track/TrackUploadForm.vue'
import PlatformsPanel from '@/components/dashboard/PlatformsPanel.vue'

const authStore = useAuthStore()
const tracksStore = useTracksStore()

const isContractModalOpen = ref(false)
const activeDraftId = ref<string | null>(null)
const searchQuery = ref('')
const platforms = ref(['Total', 'ЯМ', 'VK', 'Apple', 'Spotify'])
const activePlatform = ref('Total')

const displayedPlays = computed(() => {
  if (activePlatform.value === 'Total') return tracksStore.totalPlays
  const map: Record<string, 'spotify' | 'apple' | 'yandex' | 'vk'> = {
    Spotify: 'spotify',
    Apple: 'apple',
    'ЯМ': 'yandex',
    VK: 'vk',
  }
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
  const query = searchQuery.value.toLowerCase()
  return tracksStore.tracks.filter(track => track.title.toLowerCase().includes(query))
})

const handleContractSuccess = (payload: { release?: { title: string; type?: string; tracks?: unknown[] }; trackTitle?: string }) => {
  isContractModalOpen.value = false
  const rel = payload?.release
  const title = rel?.title || payload?.trackTitle || 'Новый релиз'
  const newTrackId = tracksStore.createFromRelease({
    title,
    type: rel?.type,
    trackCount: rel?.tracks?.length ?? 1,
  })
  activeDraftId.value = newTrackId
}
const continueDraft = (trackId: string) => { activeDraftId.value = trackId }
const onTrackUploaded = (trackId: string) => {
  tracksStore.completeTrackUpload(trackId)
  activeDraftId.value = null
}

onMounted(() => { tracksStore.fetchTracks() })
</script>
