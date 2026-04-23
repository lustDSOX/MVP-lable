<template>
  <div class="min-h-screen bg-[#050505] font-mono text-[#e0e0e0] relative overflow-hidden selection:bg-[#00ffff] selection:text-black">
    <!-- Фоновый декоративный элемент (Neo-Tribal/Wireframe vibe) -->
    <div class="fixed top-0 left-0 w-full h-full pointer-events-none opacity-20 z-0 bg-[radial-gradient(circle_at_center,_transparent_0%,_#000_100%),linear-gradient(0deg,_#111_1px,_transparent_1px),linear-gradient(90deg,_#111_1px,_transparent_1px)] bg-[size:100%_100%,_40px_40px,_40px_40px]"></div>

    <div class="max-w-[1400px] mx-auto px-6 pt-8 pb-16 relative z-10">
      
      <!-- HEADER & LOGOUT -->
      <header class="flex justify-between items-end mb-12 border-b-2 border-[#333] pb-4">
        <div>
          <h1 class="text-5xl font-black tracking-tighter chrome-text mb-1 uppercase">
            {{ authStore.artistName || 'SYS.MODERATOR' }}
          </h1>
          <p class="text-[#00ffff] text-sm tracking-widest uppercase">>>> Global_Release_Control_Center</p>
        </div>
        <button @click="logout" class="y2k-btn logout-btn flex items-center gap-2">
          <span>[ LOGOUT ]</span>
          <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="square" stroke-linejoin="miter" stroke-width="2" d="M17 16l4-4m0 0l-4-4m4 4H7m6 4v1a3 3 0 01-3 3H6a3 3 0 01-3-3V7a3 3 0 013-3h4a3 3 0 013 3v1"></path></svg>
        </button>
      </header>

      <!-- КОМАНДНАЯ ПАНЕЛЬ (ТАБЫ И ПОИСК) -->
      <section class="flex flex-col md:flex-row justify-between items-start md:items-center gap-6 mb-8">
        <div class="flex gap-4">
          <button 
            @click="activeTab = 'pending'" 
            class="tab-btn" 
            :class="{ 'active': activeTab === 'pending' }">
            PENDING_QUEUE [{{ pendingCount }}]
          </button>
          <button 
            @click="activeTab = 'processed'" 
            class="tab-btn" 
            :class="{ 'active': activeTab === 'processed' }">
            PROCESSED_HISTORY
          </button>
        </div>

        <div class="relative w-full md:w-96">
          <div class="absolute inset-y-0 left-0 flex items-center pl-3 pointer-events-none">
            <span class="text-[#00ffff]">/></span>
          </div>
          <input
            type="text"
            v-model="searchQuery"
            class="w-full bg-black border-2 border-[#555] text-white pl-10 pr-4 py-2 focus:outline-none focus:border-[#00ffff] transition-colors uppercase placeholder-[#444]"
            placeholder="SEARCH RELEASES..."
          />
        </div>
      </section>

      <!-- ТАБЛИЦА РЕЛИЗОВ -->
      <section class="neo-container">
        <div class="overflow-x-auto">
          <table class="w-full text-left min-w-[900px] border-collapse">
           <thead>
              <tr class="border-b-2 border-[#333] text-[#888] text-xs tracking-widest uppercase">
                <th class="p-4">Cover</th>
                <th class="p-4">Release Info</th>
                <!-- Фильтр по типу -->
                <th class="p-4">
                  Type / Tracks
                  <select v-model="typeFilter" class="ml-2 bg-black border border-[#333] text-[#00ffff] text-[10px] outline-none cursor-pointer">
                    <option value="ALL">ALL</option>
                    <option value="SINGLE">SINGLE</option>
                    <option value="EP">EP</option>
                    <option value="ALBUM">ALBUM</option>
                  </select>
                </th>
                <!-- Сортировка по дате -->
                <th class="p-4 cursor-pointer hover:text-[#00ffff] transition-colors select-none" @click="toggleDateSort" title="Click to sort">
                  Date Sub/Proc
                  <span v-if="sortOrder === 'desc'" class="ml-1 text-[#00ffff]">▼</span>
                  <span v-else-if="sortOrder === 'asc'" class="ml-1 text-[#00ffff]">▲</span>
                  <span v-else class="ml-1 opacity-50">↕</span>
                </th>
                <th class="p-4 text-center">Status</th>
                <th class="p-4 text-right">Action</th>
              </tr>
            </thead>
            <tbody>
              <tr v-if="filteredReleases.length === 0">
                <td colspan="6" class="p-12 text-center text-[#555] text-xl">NO DATA FOUND MATCHING CRITERIA_</td>
              </tr>
              <tr 
                v-for="release in filteredReleases" 
                :key="release.id" 
                class="border-b border-[#222] hover:bg-[#111] transition-colors"
              >
                <td class="p-4 w-20">
                   <div class="w-16 h-16 border border-[#555] p-1 bg-black">
                     <img :src="release.image || '/placeholder-cover.png'" class="w-full h-full object-cover grayscale contrast-125" alt="Cover">
                   </div>
                </td>
                <td class="p-4">
                  <h3 class="text-white font-bold text-lg uppercase tracking-wide">{{ release.title }}</h3>
                  <span class="text-[#00ffff] text-sm">{{ release.owner?.name || 'UNKNOWN' }}</span>
                </td>
                <td class="p-4 text-sm text-[#888]">
                  <span class="text-white">{{ getReleaseType(release.tracks?.length) }}</span><br/>
                  {{ release.tracks?.length || 0 }} TRK(s)
                </td>
                <td class="p-4 text-sm text-[#888]">
                  {{ formatDate(release.created_at) }}
                </td>
                <td class="p-4 text-center">
                  <span class="status-badge" :class="release.status">
                    {{ release.status }}
                  </span>
                </td>
                <td class="p-4 text-right">
                  <button 
                    v-if="release.status === 'pending'" 
                    @click="openReviewModal(release)" 
                    class="y2k-btn action-btn bg-[#2563eb]">
                    [ REVIEW_MODERATION ]
                  </button>
                  <button 
                    v-else 
                    @click="openHistoryModal(release)" 
                    class="y2k-btn action-btn bg-[#333]">[ VIEW_LOGS ]
                  </button>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </section>

    </div>

    <!-- МОДАЛЬНОЕ ОКНО РЕВЬЮ РЕЛИЗА И ТРЕКОВ -->
    <Teleport to="body">
      <!-- ЕДИНОЕ МОДАЛЬНОЕ ОКНО ДЛЯ РЕВЬЮ И ИСТОРИИ -->
      <div v-if="selectedRelease && isReviewModalOpen" class="fixed inset-0 bg-black/95 flex justify-center items-center z-[9999] p-4 backdrop-blur-sm">
        
        <div class="w-full max-w-[1500px] h-[90vh] bg-black border-2 border-[#555] shadow-[4px_4px_0_#333] flex flex-col relative">
          
          <!-- HEADER -->
          <div class="flex justify-between items-center p-4 border-b-2 border-[#333] bg-[#0a0a0a]">
            <div class="flex items-center gap-4">
               <h2 class="text-2xl font-bold chrome-text uppercase">{{ selectedRelease.title }}</h2>
               <span class="text-[#00ffff] text-sm tracking-widest uppercase">BY {{ selectedRelease.owner?.name }}</span>
            </div>
            <button @click="closeModals" class="text-white hover:text-red-500 z-[10000] text-4xl leading-none font-bold">&times;</button>
          </div>

          <!-- BODY (2 Columns: Tracklist & Workspace) -->
          <div class="flex flex-1 overflow-hidden">
            
            <!-- LEFT COLUMN: Tracklist Sidebar -->
            <div class="w-80 border-r-2 border-[#333] flex flex-col bg-[#050505]">
               <div class="p-4 border-b border-[#222]">
                  <!-- Cover Thumbnail -->
                  <div class="mb-3 w-full">
                    <img :src="selectedRelease.image || '/placeholder-cover.png'" class="w-full aspect-square object-cover border border-[#444]">
                  </div>
                  <div class="text-xs text-[#888] space-y-1">
                    <p>DATE: <span class="text-white">{{ formatDate(selectedRelease.release_date) }}</span></p>
                    <p>TYPE: <span class="text-white">{{ getReleaseType(selectedRelease.tracks?.length) }}</span></p>
                  </div>
               </div>
               <!-- Tracks Navigation -->
               <div class="flex-1 overflow-y-auto p-4 bg-[url('https://www.transparenttextures.com/patterns/carbon-fibre.png')]">
                 <h3 class="text-[10px] text-[#666] mb-3 uppercase tracking-widest">Select track to review:</h3>
                 <div class="space-y-2">
                   <button v-for="(track, index) in selectedRelease.tracks" :key="track.id" @click="activeTrackId = track.id" class="w-full text-left p-3 border flex items-center justify-between transition-all" :class="activeTrackId === track.id ? 'border-[#00ffff] bg-[#00ffff]/10 text-white' : 'border-[#333] text-[#888] hover:border-[#666] hover:bg-[#111]'">
                     <div class="truncate pr-2 w-3/4"> <span class="text-xs opacity-50 mr-1">{{ index + 1 }}.</span> <span class="uppercase text-sm font-bold tracking-wide">{{ track.title }}</span> </div>
                     <div class="w-1/4 text-right text-xs font-mono">
                        <span v-if="reviewState[track.id]?.status === 'approved'" class="text-[#39ff14]">[OK]</span>
                        <span v-else-if="reviewState[track.id]?.status === 'rejected'" class="text-red-500">[ERR]</span>
                        <span v-else class="text-[#666] animate-pulse">Wait..</span>
                     </div>
                   </button>
                 </div>
               </div>
            </div>

            <!-- RIGHT COLUMN: Active Track Workspace -->
            <div class="flex-1 flex flex-col bg-[#0a0a0a]" v-if="activeTrack">
               
               <!-- Track Info & Tabs -->
               <div class="p-6 border-b border-[#222] flex justify-between items-start">
                  <div>
                    <h3 class="text-4xl font-black text-white uppercase tracking-wider mb-1">{{ activeTrack.title }}</h3>
                    <p class="text-[#555] text-xs font-mono">TRACK_ID: {{ activeTrack.id }}</p>
                  </div>
                  <div class="flex gap-2" v-if="!isHistoryMode">
                    <button @click="reviewModalTab = 'review'" class="tab-btn" :class="{ 'active': reviewModalTab === 'review' }">REVIEW</button>
                    <button @click="reviewModalTab = 'history'" class="tab-btn" :class="{ 'active': reviewModalTab === 'history' }">HISTORY</button>
                  </div>
               </div>

               <!-- ########## ОБЛАСТЬ ОЦЕНКИ (v-if) ########## -->
               <div v-if="reviewModalTab === 'review' && !isHistoryMode" class="flex-1 flex flex-col">
                  <!-- Media & Lyrics Grid -->
                  <div class="p-6 flex-1 flex flex-col gap-6 overflow-y-auto">
                    <label class="flex items-center gap-3 cursor-pointer border-2 border-[#333] px-4 py-2 hover:border-[#666] transition-colors bg-black group select-none">
                        <input type="checkbox" :checked="getTrackExplicit(activeTrack.id)" @change="toggleTrackExplicit(activeTrack.id)" class="hidden">
                        <div class="w-5 h-5 border-2 border-[#555] flex items-center justify-center group-hover:border-[#00ffff] transition-colors" :class="{'border-red-500': getTrackExplicit(activeTrack.id)}">
                           <div v-if="getTrackExplicit(activeTrack.id)" class="w-3 h-3 bg-red-500"></div>
                        </div>
                        <span class="text-sm font-bold tracking-widest" :class="getTrackExplicit(activeTrack.id) ? 'text-red-500' : 'text-[#888]'"> EXPLICIT CONTENT </span>
                    </label>
                    <div class="bg-black border-2 border-[#222] p-4">
                        <span class="text-xs text-[#666] mb-2 block uppercase tracking-widest font-mono">Audio_Stream_Source</span>
                        <audio controls :src="activeTrack.preview_file || activeTrack.master_file" class="w-full h-12 outline-none"></audio>
                    </div>
                    <div class="flex-1 flex flex-col min-h-[150px]">
                        <span class="text-xs text-[#666] mb-2 block uppercase tracking-widest font-mono">Lyrics_Analysis</span>
                        <div class="bg-[#050505] border-2 border-[#222] p-4 flex-1 overflow-y-auto text-sm text-[#ccc] font-sans leading-relaxed whitespace-pre-wrap selection:bg-[#00ffff] selection:text-black">{{ activeTrack.lyrics || 'NO LYRICS PROVIDED BY THE ARTIST.' }}</div>
                    </div>
                  </div>
                  <!-- Track Verdict Panel -->
                  <div class="p-6 bg-black border-t-2 border-[#333]">
                    <div class="flex flex-col md:flex-row gap-6 items-start">
                        <div class="w-full md:w-1/3">
                            <p class="text-[10px] text-[#888] mb-2 uppercase tracking-widest">Track_Decision:</p>
                            <div class="flex gap-2">
                                <button @click="setTrackVerdict(activeTrack.id, 'approved')" class="flex-1 py-4 text-sm font-bold tracking-widest border-2 transition-all" :class="getTrackVerdict(activeTrack.id) === 'approved' ? 'bg-[#39ff14]/10 border-[#39ff14] text-[#39ff14]' : 'border-[#333] text-[#666] hover:border-[#888] hover:text-white'">APPROVE</button>
                                <button @click="setTrackVerdict(activeTrack.id, 'rejected')" class="flex-1 py-4 text-sm font-bold tracking-widest border-2 transition-all" :class="getTrackVerdict(activeTrack.id) === 'rejected' ? 'bg-red-500/10 border-red-500 text-red-500' : 'border-[#333] text-[#666] hover:border-[#888] hover:text-white'">REJECT</button>
                            </div>
                        </div>
                        <div class="w-full md:w-2/3" v-if="getTrackVerdict(activeTrack.id) === 'rejected'">
                            <p class="text-[10px] text-red-500 mb-2 uppercase tracking-widest">Rejection_Reason (Required):</p>
                            <textarea :value="getTrackComment(activeTrack.id)" @input="setTrackComment(activeTrack.id, $event)" placeholder="Specify exactly why this track is rejected..." class="w-full h-20 bg-[#050505] border-2 border-red-900 focus:border-red-500 text-red-100 text-sm p-3 resize-none outline-none transition-colors"></textarea>
                        </div>
                    </div>
                  </div>
               </div>
               
               <!-- ########## ОБЛАСТЬ ИСТОРИИ (v-else-if) ########## -->
               <div v-else-if="reviewModalTab === 'history' || isHistoryMode" class="flex-1 p-6 overflow-y-auto">
                 <h3 class="text-xl font-bold uppercase tracking-wider text-[#888] border-b border-[#333] pb-3 mb-6"> <span class="text-[#00ffff]">LOG_FILE:</span> Moderation History </h3>
                 <div v-if="!selectedRelease.moderation_logs || selectedRelease.moderation_logs.length === 0" class="h-full flex items-center justify-center"> <span class="text-[#444] font-mono text-2xl animate-pulse">NO PREVIOUS LOGS FOUND_</span> </div>
                 <div v-else class="space-y-6">
                   <div v-for="log in selectedRelease.moderation_logs" :key="log.id" class="border-l-4 border-[#333] pl-6 py-2 bg-[#111]/50">
                      <div class="flex justify-between items-center mb-2"> <span class="font-bold text-sm text-[#00ffff] uppercase">{{ log.moderator_name }}</span> <span class="text-xs text-[#666] font-mono">{{ formatDate(log.created_at) }}</span> </div>
                      <p class="text-white font-mono text-sm whitespace-pre-wrap leading-relaxed"> > {{ log.comment }} </p>
                   </div>
                 </div>
               </div>
            </div>
            
            <!-- Fallback if no track active -->
            <div class="flex-1 flex items-center justify-center bg-[#0a0a0a]" v-else>
               <span class="text-[#555] font-mono animate-pulse">SELECT A TRACK FROM THE LIST</span>
            </div>

          </div>

          <!-- FOOTER: Global Actions (Скрываем в режиме истории) -->
          <div v-if="!isHistoryMode" class="p-4 border-t-2 border-[#333] bg-black flex justify-between items-center">
             <div class="flex items-center gap-3 bg-[#111] px-4 py-2 border border-[#333]">
               <span class="text-[10px] text-[#666] uppercase tracking-widest">Global Status Calc:</span>
               <span class="font-bold uppercase text-sm" :class="computedOverallVerdict === 'rejected' ? 'text-red-500' : (computedOverallVerdict === 'approved' ? 'text-[#39ff14]' : 'text-[#888]')">{{ computedOverallVerdict === 'draft' ? 'PENDING...' : computedOverallVerdict }}</span>
             </div>
             <div class="flex gap-4">
               <button @click="saveProgress" class="px-6 py-3 text-[#00ffff] border-2 border-[#00ffff] hover:bg-[#00ffff] hover:text-black font-bold uppercase tracking-widest text-sm transition-all shadow-[0_0_10px_rgba(0,255,255,0.2)]">SAVE_DRAFT_PROGRESS</button>
               <button @click="submitReview" :disabled="!isReviewComplete" class="px-8 py-3 font-bold uppercase tracking-widest text-sm transition-all" :class="!isReviewComplete ? 'bg-[#333] text-[#666] cursor-not-allowed' : (computedOverallVerdict === 'rejected' ? 'bg-red-500 text-white hover:brightness-125 shadow-[0_0_15px_rgba(239,68,68,0.4)]' : 'bg-[#39ff14] text-black hover:brightness-125 shadow-[0_0_15px_rgba(57,255,20,0.4)]')">COMMIT_FINAL_VERDICT</button>
             </div>
          </div>

        </div>
      </div>
    </Teleport>
  </div>

</template>

<script lang="ts">
import { defineComponent } from 'vue';
import { useAuthStore } from '@/stores/auth'; // Настройте пути под ваш проект
import { useModerationStore, type ReleaseForModeration } from '@/stores/moderation';

// Описываем треки (в вашем сторе ReleaseForModeration их пока нет, поэтому мы расширяем тип локально)
interface Track {
  id: number;
  release_id: number;
  title: string;
  order: number;
  master_file: string;
  preview_file: string;
  lyrics: string;
  is_explicit: boolean;
  moderation_comment?: string;
}

interface ModerationLog {
  id: number;
  moderator_name: string;
  comment: string;
  created_at: string;
}

interface ExtendedRelease extends ReleaseForModeration {
  tracks: Track[];
  moderation_logs?: ModerationLog[]; // Логи теперь часть релиза
}

interface TrackReviewState {
  status: 'approved' | 'rejected' | null;
  comment: string;
  is_explicit: boolean; 
}

export default defineComponent({
  name: 'ModeratorCabinet',
  
  // Подключаем сторы через setup() для Options API
  setup() {
    const authStore = useAuthStore();
    const moderationStore = useModerationStore();
    
    return {
      authStore,
      moderationStore
    };
  },

  data() {
    return {
      activeTab: 'pending' as 'pending' | 'processed',
      searchQuery: '',
      isReviewModalOpen: false,
      isHistoryModalOpen: false,
      selectedRelease: null as ExtendedRelease | null,
      reviewState: {} as Record<number, TrackReviewState>,
      typeFilter: 'ALL' as 'ALL' | 'SINGLE' | 'EP' | 'ALBUM',
      sortOrder: 'desc' as 'asc' | 'desc' | null, // По умолчанию новые сверху
      activeTrackId: null as number | null,
      isHistoryMode: false, // открыта ли модалка в режиме "только чтение истории"
      reviewModalTab: 'review' as 'review' | 'history', // Активная вкладка внутри модалки
    };
  },

  watch: {
    // Блокируем скролл body при открытии любой модалки
    isAnyModalOpen(isOpen: boolean) {
      if (isOpen) {
        document.body.style.overflow = 'hidden';
      } else {
        document.body.style.overflow = '';
      }
    }
  },

  computed: {

    activeTrack(): Track | null {
      if (!this.selectedRelease || !this.selectedRelease.tracks || !this.activeTrackId) return null;
      return this.selectedRelease.tracks.find(t => t.id === this.activeTrackId) || null;
    },

    isAnyModalOpen(): boolean {
      return this.isReviewModalOpen || this.isHistoryModalOpen;
    },

    // Получаем массив из стора с приведением типа
    allReleases(): ExtendedRelease[] {
      return this.moderationStore.releases as ExtendedRelease[];
    },

    pendingCount(): number {
      return this.allReleases.filter(r => r.status === 'pending').length;
    },

    filteredReleases(): ExtendedRelease[] {
      let list = this.allReleases;
      
      // Фильтр по табам
      if (this.activeTab === 'pending') {
        list = list.filter(r => r.status === 'pending');
      } else {
        list = list.filter(r => ['approved', 'rejected', 'published'].includes(r.status));
      }

      // Фильтр по поиску
      if (this.searchQuery) {
        const q = this.searchQuery.toLowerCase();
        list = list.filter(r => 
          r.title.toLowerCase().includes(q) || 
          (r.owner?.name.toLowerCase().includes(q))
        );
      }

      // НОВОЕ: Фильтр по типу релиза
      if (this.typeFilter !== 'ALL') {
        list = list.filter(r => this.getReleaseType(r.tracks?.length) === this.typeFilter);
      }

      // НОВОЕ: Сортировка по дате (created_at)
      if (this.sortOrder) {
        list.sort((a, b) => {
          const dateA = new Date(a.created_at).getTime();
          const dateB = new Date(b.created_at).getTime();
          return this.sortOrder === 'asc' ? dateA - dateB : dateB - dateA;
        });
      }

      return list;
    },

    computedOverallVerdict(): 'approved' | 'rejected' | 'draft' {
      if (!this.selectedRelease || !this.selectedRelease.tracks) return 'draft';
      
      const tracks = this.selectedRelease.tracks;
      let allApproved = true;
      
      for (const track of tracks) {
        const state = this.reviewState[track.id];
        if (!state) return 'draft';
        if (state.status === 'rejected') return 'rejected';
        if (state.status !== 'approved') allApproved = false;
      }
      
      return allApproved ? 'approved' : 'draft';
    },

    isReviewComplete(): boolean {
        if (!this.selectedRelease || !this.selectedRelease.tracks) return false;

        // 1. Если есть хотя бы один отклоненный трек С НАПИСАННЫМ КОММЕНТАРИЕМ,
        // мы разрешаем досрочно отклонить весь релиз.
        const hasValidRejection = this.selectedRelease.tracks.some(track => {
            const state = this.reviewState[track.id];
            return state && state.status === 'rejected' && state.comment.trim() !== '';
        });
        
        if (hasValidRejection) return true;

        // 2. Если отклоненных нет, то для ОДОБРЕНИЯ релиза ВСЕ треки должны быть 'approved'
        return this.selectedRelease.tracks.every(track => {
            const state = this.reviewState[track.id];
            return state && state.status === 'approved';
        });
    }
  },

  methods: {
    
    toggleDateSort() {
      if (this.sortOrder === 'desc') {
        this.sortOrder = 'asc';
      } else if (this.sortOrder === 'asc') {
        this.sortOrder = null;
      } else {
        this.sortOrder = 'desc';
      }
    },

    getTrackComment(trackId: number): string {
      return this.reviewState[trackId]?.comment || '';
    },

    // Безопасное сохранение комментария
    setTrackComment(trackId: number, event: Event) {
      const target = event.target as HTMLTextAreaElement;
      if (this.reviewState[trackId]) {
        this.reviewState[trackId].comment = target.value;
      }
    },

    logout() {
      console.log('Logging out...');
      // this.authStore.logout();
    },

    formatDate(dateString: string) {
      return new Date(dateString).toLocaleDateString('en-GB', { day: '2-digit', month: 'short', year: 'numeric' }).toUpperCase();
    },

    getReleaseType(trackCount?: number) {
      if (!trackCount || trackCount === 1) return 'SINGLE';
      if (trackCount <= 6) return 'EP';
      return 'ALBUM';
    },

    getTrackExplicit(trackId: number): boolean {
      return this.reviewState[trackId]?.is_explicit || false;
    },

    // Безопасное переключение статуса Explicit
    toggleTrackExplicit(trackId: number) {
      if (this.reviewState[trackId]) {
        this.reviewState[trackId].is_explicit = !this.reviewState[trackId].is_explicit;
      }
    },

    openReviewModal(release: ExtendedRelease) {
      this.selectedRelease = release;
      this.isHistoryMode = false; // Открываем в режиме АКТИВНОЙ ОЦЕНКИ
      this.reviewModalTab = 'review'; // По умолчанию показываем вкладку оценки
      
      // Инициализируем стейт для каждого трека
      const newState: Record<number, TrackReviewState> = {};
      if (release.tracks && release.tracks.length > 0) {
        release.tracks.forEach(track => {
          newState[track.id] = { 
            status: null, 
            comment: '',
            is_explicit: track.is_explicit // Подтягиваем из БД
          };
        });
        // Автоматически выбираем первый трек при открытии
        this.activeTrackId = release.tracks[0]?.id ?? null;
      }
      this.reviewState = newState;
      this.isReviewModalOpen = true;
    },

    async saveProgress() {
      if (!this.selectedRelease) return;
      
      // Собираем текущий прогресс
      const progressPayload = {
        releaseId: this.selectedRelease.id,
        tracks: Object.entries(this.reviewState).map(([id, state]) => ({
          track_id: Number(id),
          status: state.status,
          comment: state.comment,
          is_explicit: state.is_explicit
        }))
      };

      console.log('SAVING DRAFT PROGRESS...', progressPayload);
      
      // TODO: Отправка на ваш API
      // await this.moderationStore.saveDraftProgress(progressPayload);
      
      alert('PROGRESS SAVED LOCALLY! \n(Check console for payload)');
    },

    openHistoryModal(release: ExtendedRelease) {
        this.selectedRelease = release;
        this.isHistoryMode = true; // Открываем в режиме ПРОСМОТРА ИСТОРИИ
        this.isReviewModalOpen = true; // Используем ту же переменную модалки
        if (release.tracks && release.tracks.length > 0) {
            this.activeTrackId = release.tracks[0]?.id ?? null; // Выбираем первый трек для показа
        }
    },

    closeModals() {
      this.isReviewModalOpen = false;
      this.selectedRelease = null;
      this.activeTrackId = null;
      this.isHistoryMode = false; // Сбрасываем режим при закрытии
    },

    setTrackVerdict(trackId: number, status: 'approved' | 'rejected') {
      if (!this.reviewState[trackId]) return;
      this.reviewState[trackId].status = status;
      
      // Очищаем комментарий при аппруве
      if (status === 'approved') {
        this.reviewState[trackId].comment = '';
      }
    },

    getTrackVerdict(trackId: number) {
      return this.reviewState[trackId]?.status;
    },

    async submitReview() {
      if (!this.isReviewComplete || !this.selectedRelease) return;
      const finalStatus = this.computedOverallVerdict;
      
      // В реальном API вам нужно будет передавать и финальные статусы треков,
      // и их обновленный флаг is_explicit. 
      console.log("FINAL SUBMIT:", this.reviewState);

      if (finalStatus === 'rejected') {
        const combinedReasons = Object.values(this.reviewState)
          .filter(state => state.status === 'rejected')
          .map(state => state.comment)
          .join(' | ');
        await this.moderationStore.rejectRelease(this.selectedRelease.id, combinedReasons);
      } else if (finalStatus === 'approved') {
        await this.moderationStore.approveRelease(this.selectedRelease.id);
      }
      
      this.closeModals();
    },
},

async mounted() {
    await this.moderationStore.fetchQueue();

    this.moderationStore.releases = [
    {
        id: 1, title: 'SYSTEM_FAILURE', status: 'pending', owner: { id: 10, name: 'Glitch Mob' }, 
        created_at: '2026-04-21T10:00:00Z', release_date: '2026-05-01T00:00:00Z',
        image: 'https://images.unsplash.com/photo-1614729939124-032f0b56c9ce?q=80&w=1000',
        tracks:[
            { id: 101, release_id: 1, title: 'Error 404', order: 1, master_file: '', preview_file: 'https://www.soundhelix.com/examples/mp3/SoundHelix-Song-1.mp3', lyrics: 'Connection lost...', is_explicit: false },
            { id: 102, release_id: 1, title: 'Kernel Panic', order: 2, master_file: '', preview_file: 'https://www.soundhelix.com/examples/mp3/SoundHelix-Song-2.mp3', lyrics: 'Core dumped.', is_explicit: true }
        ],
        moderation_logs: []
    },
    {
        id: 2, title: 'Neon Pulse', status: 'pending', owner: { id: 12, name: 'GridRunner' }, 
        created_at: '2026-04-19T12:30:00Z', release_date: '2026-05-05T00:00:00Z',
        image: 'https://images.unsplash.com/photo-1557672172-298e090bd0f1?q=80&w=1000',
        tracks:[
            { id: 201, release_id: 2, title: 'Intro', order: 1, master_file: '', preview_file: 'https://www.soundhelix.com/examples/mp3/SoundHelix-Song-8.mp3', lyrics: '[Instrumental]', is_explicit: false }
        ],
        moderation_logs: [
            { id: 1, moderator_name: 'SYS.MODERATOR', comment: 'Release rejected. Reason: Intro track has low bitrate audio.', created_at: '2026-04-15T18:00:00Z' }
        ]
    },
    {
        id: 3, title: 'Chrome Tear', status: 'rejected', owner: { id: 15, name: 'Y2K Princess' }, 
        created_at: '2026-04-10T12:00:00Z', release_date: '2026-04-15T00:00:00Z',
        image: 'https://images.unsplash.com/photo-1518066000714-58c45f1a2c08?q=80&w=1000',
        tracks:[
            { id: 301, release_id: 3, title: 'Sad Machine', order: 1, master_file: '', preview_file: '', lyrics: 'Crying in the club...', is_explicit: false, moderation_comment: 'Audio clipping at 0:45. Please fix mastering.' }
        ],
        moderation_logs: [
            { id: 2, moderator_name: 'SYS.MODERATOR', comment: 'Release rejected. Reason: Track "Sad Machine" has audio clipping at 0:45. Please fix mastering.', created_at: '2026-04-11T11:30:00Z' }
        ]
    }
    ] as any;
  },

  // Защита: гарантированно возвращаем скролл при уходе со страницы
  beforeUnmount() {
    document.body.style.overflow = '';
  }
});
</script>

<style scoped>
/* Y2K / Chrome / Neo-Tribal Эстетика */

.chrome-text {
  background: linear-gradient(to bottom, #ffffff 0%, #aaaaaa 40%, #555555 50%, #e0e0e0 55%, #ffffff 100%);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  filter: drop-shadow(0px 2px 2px rgba(255, 255, 255, 0.2));
}

.y2k-btn {
  font-family: 'Courier New', Courier, monospace;
  font-weight: bold;
  padding: 0.5rem 1rem;
  text-transform: uppercase;
  border: 1px solid #555;
  transition: all 0.2s ease;
  position: relative;
}

.y2k-btn::before {
  content: '';
  position: absolute;
  top: 2px; left: 2px; right: -4px; bottom: -4px;
  border: 1px solid #333;
  z-index: -1;
  transition: all 0.2s ease;
}

.y2k-btn:hover {
  background-color: #fff;
  color: #000;
  border-color: #fff;
}
.y2k-btn:hover::before {
  top: 4px; left: 4px; right: -6px; bottom: -6px;
  border-color: #00ffff;
}

.tab-btn {
  background: transparent;
  color: #666;
  font-weight: bold;
  padding: 0.5rem 1rem;
  border-bottom: 2px solid transparent;
  transition: all 0.3s ease;
}
.tab-btn:hover { color: #fff; }
.tab-btn.active {
  color: #00ffff;
  border-bottom: 2px solid #00ffff;
  text-shadow: 0 0 8px rgba(0, 255, 255, 0.5);
}

.neo-container {
  background-color: rgba(10, 10, 10, 0.8);
  border: 2px solid #333;
  box-shadow: 4px 4px 0px #111;
  backdrop-filter: blur(4px);
}

.status-badge {
  display: inline-block;
  padding: 0.25rem 0.5rem;
  font-size: 0.75rem;
  font-weight: bold;
  text-transform: uppercase;
  border: 1px solid;
}
.status-badge.pending { color: #facc15; border-color: #facc15; background: rgba(250, 204, 21, 0.1); }
.status-badge.approved { color: #39ff14; border-color: #39ff14; background: rgba(57, 255, 20, 0.1); }
.status-badge.rejected { color: #ef4444; border-color: #ef4444; background: rgba(239, 68, 68, 0.1); }
.status-badge.published { color: #00ffff; border-color: #00ffff; background: rgba(0, 255, 255, 0.1); }

/* Стилизация скроллбара под Y2K */
::-webkit-scrollbar { width: 8px; }
::-webkit-scrollbar-track { background: #000; border-left: 1px solid #333; }
::-webkit-scrollbar-thumb { background: #555; border: 1px solid #000; }
::-webkit-scrollbar-thumb:hover { background: #00ffff; }
</style>