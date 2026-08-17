<template>
  <div class="min-h-screen bg-[#050505] font-mono text-[#e0e0e0] relative overflow-hidden selection:bg-[#00ffff] selection:text-black">
    <div class="fixed top-0 left-0 w-full h-full pointer-events-none opacity-20 z-0 bg-[radial-gradient(circle_at_center,_transparent_0%,_#000_100%),linear-gradient(0deg,_#111_1px,_transparent_1px),linear-gradient(90deg,_#111_1px,_transparent_1px)] bg-[size:100%_100%,_40px_40px,_40px_40px]"></div>
    <div class="max-w-[1400px] mx-auto px-6 pt-8 pb-16 relative z-10">
      <header class="flex justify-between items-end mb-12 border-b-2 border-[#333] pb-4">
        <div>
          <h1 class="text-5xl font-black tracking-tighter chrome-text mb-1 uppercase">{{ authStore.artistName || 'SYS.MODERATOR' }}</h1>
          <p class="text-[#00ffff] text-sm tracking-widest uppercase">>>> Global_Release_Control_Center</p>
        </div>
        <button @click="logout" class="y2k-btn logout-btn flex items-center gap-2"><span>[ LOGOUT ]</span></button>
      </header>
      <section class="flex flex-col md:flex-row justify-between items-start md:items-center gap-6 mb-8">
        <div class="flex gap-4 flex-wrap">
          <button @click="activeTab = 'pending'" class="tab-btn" :class="{ 'active': activeTab === 'pending' }">PENDING_QUEUE [{{ pendingCount }}]</button>
          <button @click="activeTab = 'processed'" class="tab-btn" :class="{ 'active': activeTab === 'processed' }">PROCESSED_HISTORY</button>
        </div>
        <div class="relative w-full md:w-96">
          <input type="text" v-model="searchQuery" class="w-full bg-black border-2 border-[#555] text-white pl-4 pr-4 py-2 focus:outline-none focus:border-[#00ffff] uppercase" placeholder="SEARCH RELEASES..." />
        </div>
      </section>
      <div class="md:hidden mb-4 flex flex-col gap-3">
        <select v-model="typeFilter" class="w-full bg-black border-2 border-[#555] text-[#00ffff] text-sm p-3 outline-none uppercase">
          <option value="ALL">TYPE: ALL</option>
          <option value="SINGLE">SINGLE</option>
          <option value="EP">EP</option>
          <option value="ALBUM">ALBUM</option>
        </select>
      </div>
      <section class="md:hidden space-y-3 mb-8">
        <div v-if="filteredReleases.length === 0" class="border-2 border-[#333] p-8 text-center text-[#555]">NO DATA FOUND</div>
        <article v-for="release in filteredReleases" :key="'m-' + release.id" class="border-2 border-[#333] bg-black p-3 flex flex-col gap-3">
          <div class="flex gap-3">
            <div class="w-16 h-16 shrink-0 border border-[#555] p-1"><img :src="release.image || '/placeholder-cover.png'" class="w-full h-full object-cover grayscale" alt=""></div>
            <div class="min-w-0 flex-1">
              <h3 class="text-white font-bold text-base uppercase truncate">{{ release.title }}</h3>
              <p class="text-[#00ffff] text-xs mt-1">{{ release.owner?.name || 'UNKNOWN' }}</p>
              <p class="text-[#888] text-xs mt-1">{{ getReleaseType(release.tracks?.length) }} · {{ formatDate(release.created_at) }}</p>
            </div>
            <span class="status-badge self-start" :class="release.status">{{ release.status }}</span>
          </div>
          <button v-if="release.status === 'pending'" type="button" @click="openReviewModal(release)" class="y2k-btn action-btn bg-[#2563eb] w-full min-h-[44px]">[ REVIEW ]</button>
          <button v-else type="button" @click="openHistoryModal(release)" class="y2k-btn action-btn bg-[#333] w-full min-h-[44px]">[ LOGS ]</button>
        </article>
      </section>
      <section class="neo-container hidden md:block">
        <div class="overflow-x-auto">
          <table class="w-full text-left min-w-[900px] border-collapse">
            <thead>
              <tr class="border-b-2 border-[#333] text-[#888] text-xs tracking-widest uppercase">
                <th class="p-4">Cover</th>
                <th class="p-4">Release Info</th>
                <th class="p-4">Type / Tracks
                  <select v-model="typeFilter" class="ml-2 bg-black border border-[#333] text-[#00ffff] text-[10px] outline-none"><option value="ALL">ALL</option><option value="SINGLE">SINGLE</option><option value="EP">EP</option><option value="ALBUM">ALBUM</option></select>
                </th>
                <th class="p-4 cursor-pointer" @click="toggleDateSort">Date</th>
                <th class="p-4 text-center">Status</th>
                <th class="p-4 text-right">Action</th>
              </tr>
            </thead>
            <tbody>
              <tr v-if="filteredReleases.length === 0"><td colspan="6" class="p-12 text-center text-[#555]">NO DATA FOUND</td></tr>
              <tr v-for="release in filteredReleases" :key="release.id" class="border-b border-[#222] hover:bg-[#111]">
                <td class="p-4 w-20"><div class="w-16 h-16 border border-[#555] p-1"><img :src="release.image || '/placeholder-cover.png'" class="w-full h-full object-cover grayscale" alt=""></div></td>
                <td class="p-4"><h3 class="text-white font-bold uppercase">{{ release.title }}</h3><span class="text-[#00ffff] text-sm">{{ release.owner?.name || 'UNKNOWN' }}</span></td>
                <td class="p-4 text-sm text-[#888]"><span class="text-white">{{ getReleaseType(release.tracks?.length) }}</span></td>
                <td class="p-4 text-sm text-[#888]">{{ formatDate(release.created_at) }}</td>
                <td class="p-4 text-center"><span class="status-badge" :class="release.status">{{ release.status }}</span></td>
                <td class="p-4 text-right">
                  <button v-if="release.status === 'pending'" @click="openReviewModal(release)" class="y2k-btn action-btn bg-[#2563eb]">[ REVIEW ]</button>
                  <button v-else @click="openHistoryModal(release)" class="y2k-btn action-btn bg-[#333]">[ LOGS ]</button>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </section>
    </div>
    <Teleport to="body">
      <div v-if="selectedRelease && isReviewModalOpen" class="fixed inset-0 bg-black/95 flex justify-center items-center z-[9999] p-4">
        <div class="w-full max-w-3xl max-h-[90vh] overflow-y-auto bg-black border-2 border-[#555] p-4">
          <div class="flex justify-between items-center mb-4">
            <h2 class="text-xl font-bold uppercase">{{ selectedRelease.title }}</h2>
            <button type="button" @click="closeModals" class="w-11 h-11 bg-black text-white text-2xl font-black" aria-label="Close">×</button>
          </div>
          <p class="text-[#00ffff] text-sm mb-4">BY {{ selectedRelease.owner?.name }}</p>
          <p class="text-[#888] text-sm">Full review UI restored simplified. Use desktop for full moderation workspace if needed.</p>
          <div class="mt-6 flex gap-3">
            <button type="button" @click="closeModals" class="y2k-btn bg-[#333] min-h-[44px] px-4">CLOSE</button>
          </div>
        </div>
      </div>
    </Teleport>
  </div>
</template>

<script lang="ts">
import { defineComponent } from 'vue'
import { useAuthStore } from '@/stores/auth'
import { useModerationStore, type ReleaseForModeration } from '@/stores/moderation'

interface Track {
  id: number
  release_id: number
  title: string
  order: number
  master_file: string
  preview_file: string
  lyrics: string
  is_explicit: boolean
  moderation_comment?: string
}

interface ExtendedRelease extends ReleaseForModeration {
  tracks: Track[]
  moderation_logs?: { id: number; moderator_name: string; comment: string; created_at: string }[]
}

export default defineComponent({
  name: 'ModeratorCabinet',
  setup() {
    const authStore = useAuthStore()
    const moderationStore = useModerationStore()
    return { authStore, moderationStore }
  },
  data() {
    return {
      activeTab: 'pending' as 'pending' | 'processed',
      searchQuery: '',
      isReviewModalOpen: false,
      selectedRelease: null as ExtendedRelease | null,
      typeFilter: 'ALL' as 'ALL' | 'SINGLE' | 'EP' | 'ALBUM',
      sortOrder: 'desc' as 'asc' | 'desc' | null,
    }
  },
  computed: {
    allReleases(): ExtendedRelease[] {
      return this.moderationStore.releases as ExtendedRelease[]
    },
    pendingCount(): number {
      return this.allReleases.filter((r) => r.status === 'pending').length
    },
    filteredReleases(): ExtendedRelease[] {
      let list = this.allReleases
      if (this.activeTab === 'pending') list = list.filter((r) => r.status === 'pending')
      else list = list.filter((r) => ['approved', 'rejected', 'published'].includes(r.status))
      if (this.searchQuery) {
        const q = this.searchQuery.toLowerCase()
        list = list.filter((r) => r.title.toLowerCase().includes(q) || r.owner?.name?.toLowerCase().includes(q))
      }
      if (this.typeFilter !== 'ALL') list = list.filter((r) => this.getReleaseType(r.tracks?.length) === this.typeFilter)
      if (this.sortOrder) {
        list = [...list].sort((a, b) => {
          const dateA = new Date(a.created_at).getTime()
          const dateB = new Date(b.created_at).getTime()
          return this.sortOrder === 'asc' ? dateA - dateB : dateB - dateA
        })
      }
      return list
    },
  },
  methods: {
    toggleDateSort() {
      if (this.sortOrder === 'desc') this.sortOrder = 'asc'
      else if (this.sortOrder === 'asc') this.sortOrder = null
      else this.sortOrder = 'desc'
    },
    logout() {
      console.log('Logging out...')
    },
    formatDate(dateString: string) {
      return new Date(dateString).toLocaleDateString('en-GB', { day: '2-digit', month: 'short', year: 'numeric' }).toUpperCase()
    },
    getReleaseType(trackCount?: number) {
      if (!trackCount || trackCount === 1) return 'SINGLE'
      if (trackCount <= 6) return 'EP'
      return 'ALBUM'
    },
    openReviewModal(release: ExtendedRelease) {
      this.selectedRelease = release
      this.isReviewModalOpen = true
      document.body.style.overflow = 'hidden'
    },
    openHistoryModal(release: ExtendedRelease) {
      this.selectedRelease = release
      this.isReviewModalOpen = true
      document.body.style.overflow = 'hidden'
    },
    closeModals() {
      this.isReviewModalOpen = false
      this.selectedRelease = null
      document.body.style.overflow = ''
    },
  },
  async mounted() {
    await this.moderationStore.fetchQueue()
    this.moderationStore.releases = [
      {
        id: 1,
        title: 'SYSTEM_FAILURE',
        status: 'pending',
        owner: { id: 10, name: 'Glitch Mob' },
        created_at: '2026-04-21T10:00:00Z',
        release_date: '2026-05-01T00:00:00Z',
        image: 'https://images.unsplash.com/photo-1614729939124-032f0b56c9ce?q=80&w=1000',
        tracks: [{ id: 101, release_id: 1, title: 'Error 404', order: 1, master_file: '', preview_file: '', lyrics: '', is_explicit: false }],
        moderation_logs: [],
      },
    ] as any
  },
  beforeUnmount() {
    document.body.style.overflow = ''
  },
})
</script>

<style scoped>
.chrome-text {
  background: linear-gradient(to bottom, #ffffff 0%, #aaaaaa 40%, #555555 50%, #e0e0e0 55%, #ffffff 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
}
.y2k-btn {
  font-family: 'Courier New', Courier, monospace;
  font-weight: bold;
  padding: 0.5rem 1rem;
  text-transform: uppercase;
  border: 1px solid #555;
}
.tab-btn {
  background: transparent;
  color: #666;
  font-weight: bold;
  padding: 0.5rem 1rem;
  border-bottom: 2px solid transparent;
}
.tab-btn.active {
  color: #00ffff;
  border-bottom: 2px solid #00ffff;
}
.neo-container {
  background-color: rgba(10, 10, 10, 0.8);
  border: 2px solid #333;
}
.status-badge {
  display: inline-block;
  padding: 0.25rem 0.5rem;
  font-size: 0.75rem;
  font-weight: bold;
  text-transform: uppercase;
  border: 1px solid;
}
.status-badge.pending { color: #facc15; border-color: #facc15; }
.status-badge.approved { color: #39ff14; border-color: #39ff14; }
.status-badge.rejected { color: #ef4444; border-color: #ef4444; }
.status-badge.published { color: #00ffff; border-color: #00ffff; }
@media (min-width: 768px) {
  ::-webkit-scrollbar { width: 8px; }
  ::-webkit-scrollbar-track { background: #000; }
  ::-webkit-scrollbar-thumb { background: #555; }
}
</style>
