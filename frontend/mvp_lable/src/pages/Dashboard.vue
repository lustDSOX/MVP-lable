<template>
  <!-- ОСНОВНОЙ КОНТЕЙНЕР: Стиль "Студийный терминал" -->
  <div class="min-h-screen bg-[#050505] text-white pt-24 px-4 pb-12 font-['Impact','Arial_Black',sans-serif] selection:bg-[#39FF14] selection:text-black overflow-hidden relative">

    <div class="max-w-7xl mx-auto flex flex-col gap-8 relative z-10">
      
      <!-- WELCOME HEADER: Системный лог -->
      <section class="border-l-8 border-[#ff0000] pl-6 py-2 bg-black/50 shadow-[10px_10px_0_#111] flex items-center justify-between overflow-hidden">
        <div>
           <div class="text-xs font-mono text-[#ff0000] animate-pulse mb-1">SESSION_ACTIVE // UPLINK_STABLE</div>
           <h1 class="text-7xl lg:text-8xl  uppercase tracking-tight leading-none scale-y-125">
             ACCESS_USER: <span class="text-[#39FF14]">{{ authStore.artistName || 'UNKNOWN_ARTIST' }}</span>
           </h1>
        </div>
        <!-- Декор: Вращающийся индикатор загрузки -->
        <div class="hidden md:block w-16 h-16 border-4 border-dashed border-[#333] rounded-full animate-spin opacity-20 mr-6"></div>
      </section>

      <!-- АНАЛИТИКА: Виджеты как VFD-дисплеи (магнитола 2000-х) -->
      <section class="grid grid-cols-1 md:grid-cols-2 gap-6">
        <!-- Прослушивания -->
        <div class="relative bg-black border-4 border-[#222] p-6 shadow-[inset_0_0_30px_rgba(57,255,20,0.05)] group">
          <div class="absolute top-2 right-4 text-sm font-mono text-gray-700">UNIT_01: AUDIO_TRAFFIC</div>
          <span class="text-base uppercase  text-[#39FF14] tracking-wider mb-4 block italic ">TOTAL_PLAYS_COUNT</span>
          <div class="flex items-baseline gap-2">
            <span class="text-6xl  text-white tracking-tighter drop-shadow-[0_0_15px_rgba(255,255,255,0.2)]">
              {{ tracksStore.totalPlays.toLocaleString() }}
            </span>
            <span class="text-[#39FF14] text-xl animate-pulse font-mono">PLYS</span>
          </div>
          <!-- Декор: Мелкая сетка снизу -->
          <div class="absolute bottom-0 left-0 w-full h-1 bg-linear-to-r from-transparent via-[#39FF14] to-transparent opacity-20"></div>
        </div>

        <!-- Баланс -->
        <div class="relative bg-black border-4 border-[#222] p-6 shadow-[inset_0_0_30px_rgba(255,0,0,0.05)] group">
          <div class="absolute top-2 right-4 text-sm font-mono text-gray-700">UNIT_02: REVENUE_STREAM</div>
          <span class="text-base uppercase text-[#ff0000] tracking-wider mb-4 block italic ">ESTIMATED_BALANCE</span>
          <div class="flex items-baseline gap-2">
            <span class="text-6xl  text-[#39FF14] tracking-tighter drop-shadow-[0_0_15px_rgba(57,255,20,0.3)]">
              {{ tracksStore.totalRoyalties.toLocaleString() }}
            </span>
            <span class="text-white text-xl font-mono">RUB</span>
          </div>
          <div class="absolute bottom-0 left-0 w-full h-1 bg-linear-to-r from-transparent via-[#ff0000] to-transparent opacity-20"></div>
        </div>
      </section>

      <!-- ОСНОВНАЯ СЕКЦИЯ: Список релизов -->
      <section class="flex flex-col lg:flex-row gap-8 items-start">
        
        <!-- СПИСОК ТРЕКОВ -->
        <div v-if="!activeDraftId" class="flex-1 bg-black border-4 border-[#222] p-0 relative shadow-[20px_20px_0_#111]">
          <!-- Header Списка -->
          <div class="bg-[#222] p-4 flex items-center justify-between border-b-4 border-black">
            <h2 class="text-2xl  uppercase italic tracking-normal flex items-center gap-3">
              <span class="w-4 h-4 bg-[#39FF14] animate-led shadow-[0_0_10px_#39FF14]"></span>
              SYSTEM_STORAGE_RELEASES
            </h2>
            <button
              @click="isContractModalOpen = true"
              class="bg-[#39FF14] text-black  uppercase text-lg px-6 py-3 border-2 border-black shadow-[4px_4px_0_#fff] hover:shadow-none hover:translate-x-1 hover:translate-y-1 transition-none"
            >
              [+] NEW_RELEASE
            </button>
          </div>

          <div class="p-6">
            <div v-if="tracksStore.isLoading" class="text-[#39FF14] font-mono animate-pulse">>>> SCANNING_FILES...</div>
            
            <div v-else-if="tracksStore.tracks.length === 0" class="border-4 border-dashed border-[#222] p-12 text-center">
              <p class="text-gray-600 font-mono uppercase">NO_RELEASES_DETECTED. START_UPLINK_NOW.</p>
            </div>

            <ul v-else class="space-y-4">
              <li
                v-for="track in tracksStore.tracks"
                :key="track.id"
                class="bg-[#0a0a0a] border-2 border-[#222] p-4 flex flex-col gap-4 relative group hover:border-[#39FF14] transition-none"
              >
                <!-- Верхняя часть карточки трека -->
                <div class="flex items-start justify-between relative z-10">
                  <div>
                    <h3 class="text-2xl  text-white uppercase group-hover:text-[#39FF14] tracking-wide transition-none italic">{{ track.title }}</h3>
                    <span class="text-sm font-mono text-gray-500 uppercase">TRACK_ID: {{ track.id }} // PLAYS: {{ track.plays }}</span>
                  </div>
                  
                  <!-- БЕЙДЖИ СТАТУСОВ (Стиль "Световой индикатор") -->
                  <div class="flex flex-col items-end gap-1">
                    <span v-if="track.status === 'published'" class="text-base uppercase bg-[#39FF14] text-black px-2 shadow-[2px_2px_0_#fff]">
                      ONLINE
                    </span>
                    <span v-else-if="track.status === 'moderation'" class="text-base  uppercase bg-blue-600 text-white px-2 animate-pulse">
                      SCANNING
                    </span>
                    <span v-else-if="track.status === 'rejected'" class="text-base scale-y-125 uppercase bg-[#ff0000] text-white px-2 shadow-[2px_2px_0_#000]">
                      ERROR_DENIED
                    </span>
                    <span v-else-if="track.status === 'draft'" class="text-base uppercase bg-yellow-500 text-black px-2 italic">
                      PENDING_UPLINK
                    </span>
                  </div>
                </div>

                <!-- Состояние: ОТКЛОНЕН (Стиль "Системная ошибка") -->
                <div v-if="track.status === 'rejected'" class="bg-[#ff0000]/10 border border-[#ff0000] p-3 text-sm font-mono text-[#ff0000] uppercase relative overflow-hidden">
                  <div class="absolute inset-0 bg-[#790404] opacity-0 animate-pulse"></div>
                  [!] REASON: {{ track.rejectReason }}
                </div>

                <!-- Состояние: ЧЕРНОВИК -->
                <div v-if="track.status === 'draft'" class="pt-3 border-t-2 border-[#222] flex items-center justify-between">
                  <p class="text-sm font-mono text-gray-500 uppercase italic">FILES_MISSING: [WAV, COVER]</p>
                  <button 
                    @click="continueDraft(track.id)"
                    class="text-xs  uppercase text-[#39FF14] hover:bg-[#39FF14] hover:text-black px-2 py-1 border border-[#39FF14] transition-none"
                  >
                    >> RESUME_UPLINK
                  </button>
                </div>
              </li>
            </ul>
          </div>
        </div>

        <!-- ФОРМА ОТГРУЗКИ: Консоль загрузки -->
        <div v-else class="flex-1 bg-black border-4 border-[#39FF14] p-8 relative shadow-[20px_20px_0_#000] overflow-hidden">
          <div class="absolute -right-10 -top-10 text-[100px]  text-[#39FF14] opacity-[0.03] italic pointer-events-none select-none">
            UPLOAD
          </div>
          
          <button 
            @click="activeDraftId = null" 
            class="absolute top-4 right-4 text-gray-600 hover:text-[#ff0000]  uppercase text-xs transition-none flex items-center gap-2"
          >
            [X] ABORT_MISSION
          </button>
          
          <h2 class="text-4xl  uppercase italic text-[#39FF14] mb-2 leading-none">UPLINK_PROTOCOL</h2>
          <p class="text-gray-500 font-mono text-xs uppercase mb-8 border-l-2 border-[#39FF14] pl-3">
            Договор подписан. Ожидается передача бинарных данных.
          </p>
          
          <!-- Пропсы и логика сохранены -->
          <TrackUploadForm 
            :track-id="activeDraftId" 
            @track-uploaded="onTrackUploaded" 
          />
        </div>
      </section>

    </div>

    <!-- Модалка контракта: (Ожидается твой текущий компонент, просто оберни его в брутализм) -->
    <ContractModal 
      :is-open="isContractModalOpen" 
      @close="isContractModalOpen = false"
      @success="handleContractSuccess"
    />
  </div>
</template>

<style scoped>
/* Агрессивное мигание светодиода */
@keyframes real-port-flicker {
  0%, 100% { opacity: 1; filter: drop-shadow(0 0 8px #39FF14); }
  2%, 6% { opacity: 0.1; filter: none; }
  4%, 8% { opacity: 1; filter: drop-shadow(0 0 10px #39FF14); }
  42% { opacity: 0; filter: none; }
  43% { opacity: 1; }
  88% { opacity: 0.1; }
  89% { opacity: 1; }
}

.animate-led {
  animation: real-port-flicker 3s infinite steps(1);
}

/* Эффект шума старого ТВ */
.min-h-screen::after {
  content: "";
  position: absolute;
  inset: 0;
  background-image: url("data:image/svg+xml,%3Csvg viewBox='0 0 200 200' xmlns='http://www.w3.org/2000/svg'%3Ffilter id='n'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='.65'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23n)' opacity='.03'/%3E%3C/svg%3E");
  pointer-events: none;
  z-index: 50;
}
</style>

<script lang="ts">
import { defineComponent } from 'vue'
import { mapStores } from 'pinia'
import { useAuthStore } from '@/stores/auth'
import { useTracksStore } from '@/stores/tracks'

import ContractModal from '@/components/track/ContractModal.vue'
import TrackUploadForm from '@/components/track/TrackUploadForm.vue'

export default defineComponent({
  name: 'Dashboard',
  components:{
    ContractModal,
    TrackUploadForm
  },
  data() {
    return {
      isContractModalOpen: false,
      activeDraftId: null as string | null // Если null - показываем список. Если ID - форму.
    }
  },
  computed: {
    // Подключаем сторы: authStore и tracksStore
    ...mapStores(useAuthStore, useTracksStore)
  },
  mounted() {
    // При загрузке дашборда скачиваем треки
    this.tracksStore.fetchTracks()
  },
  methods: {
    handleContractSuccess(contractFormData?: any) {
      this.isContractModalOpen = false
      
      // 1. Создаем черновик трека в Pinia.
      // (В реальном проекте модалка передаст contractFormData.trackTitle, пока хардкодим)
      const title = 'Новый трек' 
      const newTrackId = this.tracksStore.createDraftContract(title)

      // 2. Сразу открываем форму загрузки файлов для этого черновика
      this.activeDraftId = newTrackId
    },

    continueDraft(trackId: string) {
      // Пользователь кликнул "Продолжить загрузку" на карточке черновика
      this.activeDraftId = trackId
    },

    onTrackUploaded(trackId: string) {
      // Форма сообщила об успехе
      this.tracksStore.completeTrackUpload(trackId)
      // Возвращаемся к списку треков
      this.activeDraftId = null
    }
  }
})
</script>