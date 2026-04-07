<template>
  <!-- Teleport выносит модалку в корень body, убирая любые лаги z-index -->
  <Teleport to="body">
    <Transition name="crt-popup">
      <div 
        v-if="isOpen" 
        class="fixed inset-0 z-9999 flex items-center justify-center p-4 sm:p-6 overflow-hidden"
        role="dialog"
        aria-modal="true"
      >
        <!-- BACKDROP: Клик только по фону закроет окно -->
        <div 
          class="absolute inset-0 bg-black/90 backdrop-blur-md cursor-pointer pointer-events-auto"
          @click.self="close"
        >
          <div class="absolute inset-0 bg-[url('https://grainy-gradients.vercel.app/noise.svg')] opacity-20 pointer-events-none"></div>
        </div>

        <!-- MODAL BODY: Стальной корпус -->
        <div 
          class="relative w-full max-w-4xl  h-screen bg-[#0a0a0a] border-[6px] border-[#333] shadow-[40px_40px_0_rgba(0,0,0,0.7)] flex flex-col font-['Impact','Arial_Black',sans-serif] selection:bg-[#39FF14] selection:text-black max-h-[95vh] overflow-hidden will-change-transform"
        >
          
          <!-- HEADER -->
          <div class="bg-[#333] p-2 flex justify-between items-center border-b-4 border-black shrink-0 relative z-50">
            <div class="flex items-center gap-3 px-2 text-[10px] font-mono tracking-widest uppercase italic">
              <div 
                class="w-3 h-3 shadow-[0_0_10px_currentColor] animate-led transition-colors duration-500"
                :class="{
                  'bg-[#39FF14] text-[#39FF14]': step === 'form',
                  'bg-blue-500 text-blue-500': step === 'preview',
                  'bg-white text-white': step === 'success'
                }"
              ></div>
              <span class="text-white">
                LEGAL_ENGINE_V.03 // STEP: {{ step.toUpperCase() }}
              </span>
            </div>
            
            <!-- Кнопка закрытия: Явно вызываем close() -->
            <button 
              type="button"
              @click="close" 
              class="bg-[#ff0000] text-black px-4 py-1 border-2 border-black hover:bg-white hover:text-black transition-none active:translate-y-1 active:translate-x-1 shadow-[2px_2px_0_#000] flex items-center gap-2 cursor-pointer pointer-events-auto"
            >
              <span class="text-xs font-black uppercase">ABORT</span>
              <span class="text-xl font-black">✖</span>
            </button>
          </div>

          <!-- CONTENT -->
          <div class="flex-1 overflow-y-auto bg-[url('https://www.transparenttextures.com/patterns/carbon-fibre.png')] relative custom-scrollbar">
            <div class="absolute top-10 left-10 text-[120px] font-black text-white opacity-[0.02] pointer-events-none select-none italic uppercase leading-none">
              SOX_LEGIT
            </div>

            <div class="p-6 md:p-10 relative z-10">
              <TrackForm 
                v-if="step === 'form'" 
                :is-open="true"
                :is-loading="isLoading" 
                @submit-form="generateContract" 
              />

              <ContractPreview 
                v-else-if="step === 'preview'" 
                :pdf-url="pdfUrl"
                :is-loading="isLoading"
                @upload-signed="uploadSignedContract"
              />

              <div v-else-if="step === 'success'" class="text-center py-12 flex flex-col items-center border-4 border-[#39FF14] bg-black/80 relative overflow-hidden group">
                <div class="absolute inset-0 bg-[#39FF14] opacity-5 animate-pulse pointer-events-none"></div>
                <div class="text-[120px] leading-none mb-6 text-[#39FF14] drop-shadow-[0_0_30px_#39FF14] italic animate-bounce-slow">✔</div>
                <h3 class="text-5xl font-black mb-4 uppercase italic tracking-tighter">MISSION_COMPLETE</h3>
                <p class="text-gray-400 font-mono text-sm mb-12 uppercase border-l-2 border-[#39FF14] px-4">
                  Договор подписан и верифицирован. <br>Система готова к приему аудио-файлов.
                </p>
                <button 
                  @click="finishAndProceed"
                  class="bg-[#39FF14] text-black font-black uppercase text-2xl px-12 py-6 border-4 border-black shadow-[10px_10px_0_#fff] hover:shadow-none hover:translate-x-1 hover:translate-y-1 transition-none"
                >
                  >> START_TRACK_UPLINK
                </button>
              </div>

              <!-- ОШИБКИ -->
              <div v-if="errorMessage" class="mt-8 p-6 bg-[#ff0000] text-black border-4 border-black animate-strobe flex items-start gap-4 shadow-[10px_10px_0_#000]">
                <span class="text-4xl font-black">[!]</span>
                <div class="flex-1">
                  <p class="text-lg font-black uppercase italic leading-none mb-1">CRITICAL_SYSTEM_ERROR</p>
                  <p class="font-mono text-xs uppercase opacity-80">{{ errorMessage }}</p>
                </div>
              </div>
            </div>
          </div>

          <!-- FOOTER -->
          <div class="bg-black border-t-4 border-[#333] p-2 flex justify-between items-center text-[8px] font-mono text-gray-700 uppercase italic shrink-0">
            <span>OS: SOX_V3_BOOTLOADER</span>
            <div class="flex gap-4">
              <span :class="isLoading ? 'text-[#39FF14] animate-pulse' : ''">UPLINK: {{ isLoading ? 'ACTIVE' : 'IDLE' }}</span>
              <span class="text-white">ENCRYPTION: AES256</span>
            </div>
            <span>© 2003 SOX HEAVY IND.</span>
          </div>
        </div>
      </div>
    </Transition>
  </Teleport>
</template>

<script lang="ts">
import { defineComponent } from 'vue'
import { mapState } from 'pinia'

import TrackForm from './TrackForm.vue'
import ContractPreview from './ContractPreview.vue'
import { useAuthStore } from '@/stores/auth';
import type { ContractFormData } from '@/types/contract';

export default defineComponent({
  name: 'ContractModal',
  components: { TrackForm, ContractPreview },
  props: {
    isOpen: { type: Boolean, required: true }
  },
  emits: ['close', 'success'],
  data() {
    return {
      step: 'form' as 'form' | 'preview' | 'success',
      isLoading: false,
      pdfUrl: '',
      errorMessage: ''
    }
  },
  computed: {
    ...mapState(useAuthStore, ['token'])
  },
  watch: {
    isOpen(newVal) {
      if (newVal) {
        this.step = 'form'
        this.pdfUrl = ''
        this.errorMessage = ''
        // Добавляем слушатель Esc при открытии
        document.addEventListener('keydown', this.handleEsc)
      } else {
        document.removeEventListener('keydown', this.handleEsc)
      }
    }
  },
  beforeUnmount() {
    document.removeEventListener('keydown', this.handleEsc)
  },
  methods: {
    handleEsc(e: KeyboardEvent) {
      if (e.key === 'Escape' && this.isOpen) this.close()
    },
    close() {
      console.log('Closing modal...') // Для дебага
      this.$emit('close')
    },
    finishAndProceed() {
      this.$emit('success')
      this.close()         
    },
    async generateContract(formData: ContractFormData) {
      this.isLoading = true
      this.errorMessage = ''
      try {
        await new Promise(res => setTimeout(res, 1500))
        this.pdfUrl = 'https://www.w3.org/WAI/ER/tests/xhtml/testfiles/resources/pdf/dummy.pdf' 
        this.step = 'preview'
      } catch (error: any) {
        this.errorMessage = error.message || 'Произошла ошибка при генерации'
      } finally {
        this.isLoading = false
      }
    },
    async uploadSignedContract(file: File) {
      this.isLoading = true
      this.errorMessage = ''
      try {
        await new Promise(res => setTimeout(res, 1500))
        this.step = 'success'
      } catch (error: any) {
        this.errorMessage = error.message || 'Ошибка загрузки файла'
      } finally {
        this.isLoading = false
      }
    }
  }
})
</script>

<style scoped>
@reference "tailwindcss";

/* Оптимизация производительности: говорим браузеру, что будет анимация */
.will-change-transform {
  will-change: transform, opacity;
}

.crt-popup-enter-active,
.crt-popup-leave-active {
  transition: all 0.3s steps(6);
}
.crt-popup-enter-from,
.crt-popup-leave-to {
  opacity: 0;
  transform: scale(0.5, 0.01); /* Эффект схлопывания в линию */
}

/* Скроллбар */
.custom-scrollbar::-webkit-scrollbar { width: 10px; }
.custom-scrollbar::-webkit-scrollbar-track { background: #000; border-left: 2px solid #222; }
.custom-scrollbar::-webkit-scrollbar-thumb { background: #333; border: 2px solid #39FF14; }

@keyframes real-port-flicker {
  0%, 100% { opacity: 1; }
  50% { opacity: 0.1; }
}
.animate-led { animation: real-port-flicker 2s infinite steps(1); }

@keyframes strobe {
  0%, 100% { background-color: #ff0000; color: #000; }
  50% { background-color: #000; color: #ff0000; }
}
.animate-strobe { animation: strobe 0.15s infinite steps(1); }
</style>