<template>
  <!-- ОСНОВНОЙ КОНТЕЙНЕР: Слот для верификации документов -->
  <div class="flex flex-col gap-8 bg-[#0a0a0a] border-4 border-[#222] p-8 shadow-[20px_20px_0_#000] font-['Impact','Arial_Black',sans-serif] text-white selection:bg-[#39FF14] selection:text-black relative overflow-hidden">
    
    <!-- HEADER: Статус файла -->
    <div class="border-b-4 border-[#39FF14] pb-4 flex items-center justify-between">
      <div>
        <h3 class="text-3xl lg:text-4xl font-black uppercase italic tracking-tighter text-white">
          CONTRACT_REVIE<span class="text-[#39FF14]">W</span>
        </h3>
        <p class="text-[10px] font-mono text-gray-500 uppercase tracking-widest">Dossier successfully compiled. Waiting for signature.</p>
      </div>
      <div class="text-right">
        <div class="text-[10px] font-mono text-[#39FF14] mb-1 animate-pulse">FILE_STATUS: READY</div>
        <div class="flex gap-1 justify-end">
          <div class="w-4 h-1 bg-[#39FF14]"></div>
          <div class="w-4 h-1 bg-[#39FF14]"></div>
          <div class="w-4 h-1 bg-[#222]"></div>
        </div>
      </div>
    </div>

    <!-- БЛОК СКАЧИВАНИЯ: Выглядит как слот для диска -->
    <div class="group relative bg-black border-4 border-[#333] p-6 flex flex-col md:flex-row items-center justify-between gap-6 hover:border-[#39FF14] transition-none overflow-hidden">
      <!-- Глитч-эффект на фоне -->
      <div class="absolute inset-0 bg-[#39FF14] opacity-0 group-hover:opacity-5 pointer-events-none"></div>
      
      <div class="flex items-center gap-6">
        <div class="w-16 h-16 bg-[#111] border-2 border-[#333] flex items-center justify-center group-hover:bg-[#39FF14] transition-none">
          <span class="text-4xl text-[#39FF14] group-hover:text-black italic font-black">PDF</span>
        </div>
        <div>
          <p class="text-sm font-mono text-gray-500 uppercase tracking-tighter mb-1">DOWNLOAD_SOURCE_DOC</p>
          <p class="text-xl font-black uppercase text-white tracking-widest">CONTRACT_V1_DRAFT.PDF</p>
        </div>
      </div>

      <a 
        :href="pdfUrl" 
        target="_blank" 
        class="w-full md:w-auto bg-white text-black font-black uppercase text-sm px-8 py-3 border-4 border-black shadow-[4px_4px_0_#39FF14] hover:shadow-none hover:translate-x-1 hover:translate-y-1 transition-none flex items-center justify-center gap-2"
      >
        <span>SAVE_TO_DISK</span>
        <span class="text-xl">💾</span>
      </a>
    </div>

    <!-- ЧЕКБОКС: Hardware Toggle -->
    <div class="flex flex-col gap-6">
      <label class="relative flex items-center gap-6 cursor-pointer group select-none">
        <!-- Кастомный чекбокс-переключатель -->
        <div class="relative w-10 h-10 bg-black border-4 border-[#333] group-hover:border-[#39FF14] flex items-center justify-center transition-none">
          <input 
            type="checkbox" 
            v-model="isAgreed" 
            class="hidden"
          />
          <!-- Неоновая галочка при выборе -->
          <div v-if="isAgreed" class="text-[#39FF14] text-3xl font-black drop-shadow-[0_0_10px_#39FF14] animate-bounce-short">✔</div>
        </div>
        
        <div class="flex-1">
          <span class="block text-lg font-black uppercase italic leading-none text-gray-400 group-hover:text-white transition-none">
            I_HAVE_READ_AND_ACCEPTED_THE_TERMS
          </span>
          <span class="text-[10px] font-mono text-[#ff0000] uppercase mt-1 block group-hover:animate-pulse">Legal verification required</span>
        </div>
      </label>

      <!-- БЛОК ЗАГРУЗКИ: Порт Uplink -->
      <Transition name="slide-up">
        <div v-if="isAgreed" class="pt-8 border-t-4 border-dashed border-[#222] flex flex-col gap-4">
          <label class="text-xs font-mono text-[#39FF14] uppercase tracking-[0.3em]">SELECT_SIGNED_SCAN_FILE (.PDF / .JPG)</label>
          
          <div class="relative group/upload">
            <!-- Скрытый инпут -->
            <input 
              type="file" 
              accept=".pdf, image/jpeg" 
              @change="onFileChange"
              id="file-upload"
              class="hidden"
            />
            <!-- Кастомная кнопка выбора -->
            <label 
              for="file-upload"
              class="flex items-center justify-between w-full px-6 py-4 bg-black border-2 border-[#333] cursor-pointer hover:border-[#ff0000] transition-none group-hover/upload:shadow-[inset_0_0_20px_rgba(255,0,0,0.1)]"
            >
              <span class="font-mono text-sm text-gray-500 uppercase italic">
                {{ selectedFile ? selectedFile.name : '>>> DRAG_OR_SELECT_FILE_FOR_UPLINK' }}
              </span>
              <div class="w-8 h-8 border-2 border-[#333] group-hover/upload:border-[#ff0000] flex items-center justify-center text-[#ff0000] font-black">
                +
              </div>
            </label>
          </div>
        </div>
      </Transition>
    </div>

    <!-- КНОПКА ОТПРАВКИ: Активация протокола -->
    <button 
      @click="submitSigned"
      :disabled="!isAgreed || !selectedFile || isLoading"
      class="w-full py-6 bg-[#39FF14] text-black font-black uppercase text-2xl border-4 border-black shadow-[10px_10px_0_#fff] hover:shadow-none hover:translate-x-1 hover:translate-y-1 active:translate-x-2 active:translate-y-2 disabled:bg-gray-800 disabled:text-gray-600 disabled:shadow-none transition-none relative group overflow-hidden"
    >
      <div class="relative z-10 flex items-center justify-center gap-4 italic tracking-tighter">
        <span v-if="!isLoading">>> EXECUTE_FINAL_UPLINK</span>
        <span v-else class="flex items-center gap-4 animate-pulse">
           <div class="w-6 h-6 border-4 border-black border-t-transparent rounded-full animate-spin"></div>
           TRANSFERRING_DATA...
        </span>
      </div>
      <!-- Глитч-вспышка -->
      <div class="absolute inset-0 bg-white opacity-0 group-hover:opacity-10 pointer-events-none"></div>
    </button>
  </div>
</template>

<style scoped>
@reference "tailwindcss";

/* Анимация галочки */
@keyframes bounce-short {
  0% { transform: scale(0.5); opacity: 0; }
  100% { transform: scale(1); opacity: 1; }
}
.animate-bounce-short {
  animation: bounce-short 0.2s cubic-bezier(0.175, 0.885, 0.32, 1.275);
}

/* Плавное появление блока загрузки */
.slide-up-enter-active, .slide-up-leave-active {
  transition: all 0.3s steps(5);
}
.slide-up-enter-from, .slide-up-leave-to {
  opacity: 0;
  transform: translateY(10px);
}

/* Кастомный фокус для инпутов (если будут) */
input:focus {
  outline: none;
}
</style>


<script lang="ts">
import { defineComponent } from 'vue'

export default defineComponent({
  name: 'ContractPreview',
  props: {
    pdfUrl: { type: String, required: true },
    isLoading: { type: Boolean, default: false }
  },
  emits: {
    'upload-signed': (file: File) => true
  },
  data() {
    return {
      isAgreed: false,
      selectedFile: null as File | null
    }
  },
  methods: {
    onFileChange(event: Event) {
      const target = event.target as HTMLInputElement
      if (target.files && target.files.length > 0) {
        this.selectedFile = target.files[0] || null
      } else {
        this.selectedFile = null
      }
    },
    submitSigned() {
      if (this.selectedFile) {
        this.$emit('upload-signed', this.selectedFile)
      }
    }
  }
})
</script>