<template>
  <form @submit.prevent="submitTrack" class="flex flex-col gap-6 text-white">
    
    <!-- 1. Аудио -->
    <div class="flex flex-col gap-2">
      <label class="font-medium uppercase tracking-wider text-sm text-gray-300">Аудиофайл (.wav) *</label>
      <input 
        type="file" accept=".wav, audio/wav" required
        @change="(e) => wavFile = (e.target as HTMLInputElement).files?.[0] || null"
        class="block w-full text-sm text-gray-400 file:mr-4 file:py-2 file:px-4 file:rounded-lg file:border-0 file:text-sm file:font-bold file:uppercase file:bg-neutral-800 file:text-[#39FF14] hover:file:bg-neutral-700 cursor-pointer border border-neutral-800 rounded-lg p-2 bg-black/50"
      />
      <!-- Показываем имя файла, если загружен -->
      <span v-if="wavFile" class="text-xs text-[#39FF14]">🎵 Загружено: {{ wavFile.name }}</span>
    </div>

    <!-- 2. Обложка с ПРЕВЬЮ -->
    <div class="flex flex-col gap-2">
      <label class="font-medium uppercase tracking-wider text-sm text-gray-300">Обложка (.jpg) *</label>
      <div class="flex items-start gap-4">
        <!-- Превью -->
        <div 
          v-if="coverPreviewUrl" 
          class="w-32 h-32 shrink-0 border border-[#39FF14] rounded-lg overflow-hidden shadow-[0_0_15px_rgba(57,255,20,0.2)]"
        >
          <img :src="coverPreviewUrl" class="w-full h-full object-cover" />
        </div>
        <div 
          v-else 
          class="w-32 h-32 shrink-0 border border-neutral-800 border-dashed rounded-lg flex items-center justify-center text-neutral-600 text-xs text-center p-2"
        >
          3000x3000px<br>RGB
        </div>
        
        <input 
          type="file" accept="image/jpeg" required
          @change="onCoverChange"
          class="block w-full text-sm text-gray-400 file:mr-4 file:py-2 file:px-4 file:rounded-lg file:border-0 file:text-sm file:font-bold file:uppercase file:bg-neutral-800 file:text-[#39FF14] hover:file:bg-neutral-700 cursor-pointer border border-neutral-800 rounded-lg p-2 bg-black/50"
        />
      </div>
    </div>

    <button 
      type="submit" 
      :disabled="isLoading || !isFormValid"
      class="w-full bg-linear-to-r from-[#39FF14] to-[#00FF00] text-black font-bold uppercase px-8 py-4 rounded-xl shadow-[0_0_20px_#39FF14] transition-all hover:scale-[1.02] disabled:opacity-50 disabled:cursor-not-allowed mt-4"
    >
      {{ isLoading ? 'Отправка...' : 'Отправить трек на модерацию' }}
    </button>
  </form>
</template>

<script lang="ts">
import { defineComponent } from 'vue'

export default defineComponent({
  name: 'TrackUploadForm',
  props: {
    trackId: { type: String, required: true } // Принимаем ID черновика
  },
  emits: ['track-uploaded'],
  data() {
    return {
      wavFile: null as File | null,
      coverFile: null as File | null,
      coverPreviewUrl: null as string | null,
      isLoading: false
    }
  },
  computed: {
    isFormValid(): boolean { return this.wavFile !== null && this.coverFile !== null }
  },
  beforeUnmount() {
    // Очищаем память браузера при закрытии формы
    if (this.coverPreviewUrl) URL.revokeObjectURL(this.coverPreviewUrl)
  },
  methods: {
    onCoverChange(e: Event) {
      const target = e.target as HTMLInputElement
      const file = target.files?.[0] || null
      this.coverFile = file
      
      if (this.coverPreviewUrl) URL.revokeObjectURL(this.coverPreviewUrl)
      if (file) {
        this.coverPreviewUrl = URL.createObjectURL(file) // Создаем ссылку на картинку
      } else {
        this.coverPreviewUrl = null
      }
    },

    async submitTrack() {
      if (!this.isFormValid) return
      this.isLoading = true
      try {
        await new Promise(res => setTimeout(res, 2000))
        this.$emit('track-uploaded', this.trackId)
      } finally {
        this.isLoading = false
      }
    }
  }
})
</script>