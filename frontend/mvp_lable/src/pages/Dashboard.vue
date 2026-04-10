<template>
  <div class="min-h-screen pt-24 px-4 pb-12 font-['Inter',sans-serif] text-white relative">
    <div class="max-w-7xl mx-auto flex flex-col gap-12 relative z-10">
      
      <!-- СЕКЦИЯ 1: КОМАНДНЫЙ ЦЕНТР -->
      <section class="command-center-grid">
        <!-- Блок приветствия (теперь на всю ширину) -->
        <div class="welcome-block">
          <h1 class="font-planet h1-metal-textured" :data-text="authStore.artistName || 'UNKNOWN'">
            {{ authStore.artistName || 'UNKNOWN' }}
          </h1>
          <span class="welcome-subtitle">Artist_Terminal</span>
        </div>

        <!-- Блок поиска (нижний левый) -->
        <div class="search-wrapper">
          <input 
            type="text" 
            v-model="searchQuery"
            placeholder="Search release by title..."
            class="search-input"
          />
        </div>

        <!-- Кнопка загрузки (нижняя правая) -->
        <button @click="isContractModalOpen = true" class="upload-button group">
          <span class="relative z-10 text-2xl">Upload New Release</span>
          <div class="absolute inset-0 crt-noise opacity-30"></div>
        </button>
      </section>

      <!-- СЕКЦИЯ 2: ПАНЕЛЬ ДАННЫХ С ВКЛАДКАМИ -->
      <section class="data-panel-container">
        <!-- Вкладки платформ -->
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
        <!-- Отображение статистики -->
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

      <!-- СЕКЦИЯ 3: ТАБЛИЦА РЕЛИЗОВ -->
      <section class="bg-black border border-[#333]">
        <div class="overflow-x-auto">
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
                      <!-- Отображение причины отказа -->
                      <div v-if="track.status === 'rejected'" class="rejection-reason">
                         REASON: {{ track.rejectReason }}
                      </div>
                   </div>
                </td>
                <td class="p-4 text-center">
                  <span v-if="track.status === 'published'" class="status-badge status-online">ONLINE</span>
                  <span v-else-if="track.status === 'moderation'" class="status-badge status-scanning animate-pulse">SCANNING</span>
                  <span v-else-if="track.status === 'rejected'" class="status-badge status-error">ERROR</span>
                  <span v-else-if="track.status === 'draft'" class="status-badge status-draft">DRAFT</span>
                </td>
                <td class="p-4 text-right font-mono text-xl">{{ track.plays.toLocaleString() }}</td>
                <td class="p-4">
                  <div v-if="track.status === 'draft'" class="flex items-center justify-center">
                    <button @click="continueDraft(track.id)" class="action-button draft-button">[CONTINUE]</button>
                  </div>
                  <div v-else class="flex items-center justify-center gap-2">
                    <button class="action-button" title="Edit Release">
                      <svg xmlns="http://www.w3.org/2000/svg" class="w-5 h-5" viewBox="0 0 20 20" fill="currentColor"><path d="M17.414 2.586a2 2 0 00-2.828 0L7 10.172V13h2.828l7.586-7.586a2 2 0 000-2.828z" /><path fill-rule="evenodd" d="M2 6a2 2 0 012-2h4a1 1 0 010 2H4v10h10v-4a1 1 0 112 0v4a2 2 0 01-2 2H4a2 2 0 01-2-2V6z" clip-rule="evenodd" /></svg>
                    </button>
                    <button class="action-button" title="View Detailed Stats">
                      <svg xmlns="http://www.w3.org/2000/svg" class="w-5 h-5" viewBox="0 0 20 20" fill="currentColor"><path d="M2 10a8 8 0 018-8v8h8a8 8 0 11-16 0z" /><path d="M12 2.252A8.014 8.014 0 0117.748 8H12V2.252z" /></svg>
                    </button>
                    <button class="action-button" title="Copy Links">
                      <svg xmlns="http://www.w3.org/2000/svg" class="w-5 h-5" viewBox="0 0 20 20" fill="currentColor"><path fill-rule="evenodd" d="M12.586 4.586a2 2 0 112.828 2.828l-3 3a2 2 0 01-2.828 0 1 1 0 00-1.414 1.414 4 4 0 005.656 0l3-3a4 4 0 00-5.656-5.656l-1.5 1.5a1 1 0 101.414 1.414l1.5-1.5zm-5 5a2 2 0 012.828 0 1 1 0 101.414-1.414 4 4 0 00-5.656 0l-3 3a4 4 0 105.656 5.656l1.5-1.5a1 1 0 10-1.414-1.414l-1.5 1.5a2 2 0 11-2.828-2.828l3-3z" clip-rule="evenodd" /></svg>
                    </button>
                  </div>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </section>
    </div>

     <!-- Модальные окна -->
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
  /* Две колонки: левая гибкая (1fr), правая фиксированная или по контенту */
  grid-template-columns: 1fr 380px; 
  gap: 2rem;
  /* Ключевое свойство: прижимает все элементы к низу их сетки */
  align-items: end; 
}

.welcome-block {
  /* Заставляет блок занимать все колонки (от 1 до последней) */
  grid-column: 1 / -1; 
  width: 100%;
  /* Выравниваем заголовок по верху, если нужно, или оставляем */
  align-self: start;
  margin-bottom: 1rem;
}

.search-wrapper {
  position: relative;
  width: 100%;
}

.upload-button {
  width: 100%;
  /* Конкретная высота или padding, чтобы кнопка была массивной */
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
  /* Чтобы кнопка не растягивалась по высоте инпута, если тот выше */
  height: fit-content; 
}

.upload-button:hover{
  box-shadow: none;
  transform: translate(2px, 2px);
}

/* Мобильная адаптация: всё в одну колонку */
@media (max-width: 1024px) {
  .command-center-grid {
    grid-template-columns: 1fr;
    gap: 1.5rem;
  }
  
  .welcome-block {
    margin-bottom: 0;
  }

  .upload-button {
    width: 100%;
    order: 3; /* Кнопка в самом низу на мобилках */
  }
}

/* Остальные ваши стили (search-input, subtitle и т.д.) */
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

.search-input:focus {
  outline: none;
  border-color: #ff0000;
}

/* Панель данных и вкладки */
.data-panel-container {
  border: 2px solid #333;
  background-color: black;
}
.platform-tabs {
  display: flex;
  border-bottom: 2px solid #333;
}
.platform-tab {
  padding: 0.75rem 1.5rem;
  font-family: 'JetBrains Mono', monospace;
  text-transform: uppercase;
  font-size: 0.875rem;
  color: #6b7280;
  border-right: 2px solid #333;
  background-color: transparent;
}
.platform-tab:last-child { border-right: none; }
.platform-tab.active {
  background-color: #ff0000;
  color: white;
}
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

/* Таблица */
.table-header { border-bottom: 2px solid #333; }
.table-th {
  padding: 1rem;
  text-transform: uppercase;
  letter-spacing: 0.1em;
  font-family: 'JetBrains Mono', monospace;
  font-size: 0.875rem;
  color: #6b7280;
}
.table-row {
  border-bottom: 1px solid #222;
  transition: background-color 0.1s;
}
.table-row:last-child { border-bottom: none; }
.table-row:hover { background-color: #0a0a0a; }

.track-title {
  font-family: 'Archivo Black', sans-serif;
  font-size: 1.25rem;
  text-transform: uppercase;
  letter-spacing: -0.025em;
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
  transition: background-color 0.2s, color 0.2s;
}
.action-button:hover {
  background-color: #ff0000;
  color: black;
}
.action-button.draft-button {
  background-color: #39FF14;
  color: black;
  font-family: 'JetBrains Mono', monospace;
  font-size: 0.75rem;
  padding: 0.5rem 0.75rem;
}
.action-button.draft-button:hover { background-color: white; }

/* Медиа-запрос для мобильных устройств */
@media (max-width: 1024px) {
  .command-center-grid {
    grid-template-columns: 1fr;
    grid-template-areas: "welcome" "search" "upload";
  }
}
@media (max-width: 768px) {
  .data-panel-content { grid-template-columns: 1fr; }
}

/* Вспомогательные классы */
.crt-noise {
  background-image: url('data:image/svg+xml;utf8,%3Csvg viewBox="0 0 200 200" xmlns="http://www.w3.org/2000/svg"%3E%3Cfilter id="noiseFilter"%3E%3CfeTurbulence type="fractalNoise" baseFrequency="0.9" numOctaves="3" stitchTiles="stitch"/%3E%3C/filter%3E%3Crect width="100%25" height="100%25" filter="url(%23noiseFilter)"/%3E%3C/svg%3E');
}
</style>

<script lang="ts" setup>
import { ref, computed, onMounted } from 'vue'
import { useAuthStore } from '@/stores/auth'
import { useTracksStore, type Track } from '@/stores/tracks'

// Импорт компонентов
import ContractModal from '@/components/track/ContractModal.vue'
import TrackUploadForm from '@/components/track/TrackUploadForm.vue'

// Инициализация
const authStore = useAuthStore()
const tracksStore = useTracksStore()

// Локальное состояние
const isContractModalOpen = ref(false)
const activeDraftId = ref<string | null>(null)
const searchQuery = ref('')
const platforms = ref(['Total', 'ЯМ', 'VK', 'Apple', 'Spotify'])
const activePlatform = ref('Total')

// --- Логика для вкладок статистики (симуляция) ---
const displayedPlays = computed(() => {
  if (activePlatform.value === 'Total') {
    return tracksStore.totalPlays
  }
  // Симуляция данных для других платформ
  const seed = platforms.value.indexOf(activePlatform.value)
  return Math.floor(tracksStore.totalPlays * (0.4 + seed * 0.1) + Math.random() * 1000)
})

const platformShare = computed(() => {
  if (activePlatform.value === 'Total' || tracksStore.totalPlays === 0) return 100
  return Math.round((displayedPlays.value / tracksStore.totalPlays) * 100)
})
// --- Конец симуляции ---

// Фильтрация треков
const filteredTracks = computed(() => {
  if (!searchQuery.value.trim()) return tracksStore.tracks
  const query = searchQuery.value.toLowerCase()
  return tracksStore.tracks.filter(track => 
    track.title.toLowerCase().includes(query)
  )
})

// Методы
const handleContractSuccess = (contractData: { trackTitle: string }) => {
  isContractModalOpen.value = false
  const title = contractData.trackTitle || 'Новый релиз'
  const newTrackId = tracksStore.createDraftContract(title)
  activeDraftId.value = newTrackId
}
const continueDraft = (trackId: string) => { activeDraftId.value = trackId }
const onTrackUploaded = (trackId: string) => {
  tracksStore.completeTrackUpload(trackId)
  activeDraftId.value = null
}

// Загрузка данных
onMounted(() => { tracksStore.fetchTracks() })
</script>