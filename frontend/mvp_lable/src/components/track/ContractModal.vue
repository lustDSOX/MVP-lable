<template>
  <Teleport to="body">
    <Transition name="crt-popup">
      <div
        v-if="isOpen"
        class="fixed inset-0 z-9999 flex items-center justify-center p-4 sm:p-6 overflow-hidden"
        role="dialog"
        aria-modal="true"
      >
        <div
          class="absolute inset-0 bg-black/90 backdrop-blur-md cursor-pointer pointer-events-auto"
          @click.self="close"
        />

        <div
          class="relative w-full max-w-4xl h-screen bg-[#0a0a0a] border-[6px] border-[#333] shadow-[40px_40px_0_rgba(0,0,0,0.7)] flex flex-col font-['Impact','Arial_Black',sans-serif] max-h-[95vh] overflow-hidden"
        >
          <div class="bg-[#333] p-2 flex justify-between items-center border-b-4 border-black shrink-0 relative z-50">
            <div class="flex items-center gap-3 px-2 text-[10px] font-mono tracking-widest uppercase italic">
              <div
                class="w-3 h-3 shadow-[0_0_10px_currentColor] animate-led transition-colors duration-500"
                :class="{
                  'bg-[#39FF14] text-[#39FF14]': step === 'form',
                  'bg-blue-500 text-blue-500': step === 'preview',
                  'bg-white text-white': step === 'success',
                }"
              />
              <span class="text-white">LEGAL_ENGINE // {{ step.toUpperCase() }} // 1_CONTRACT_PER_RELEASE</span>
            </div>
            <button
              type="button"
              class="bg-[#ff0000] text-black px-4 py-1 border-2 border-black hover:bg-white transition-none shadow-[2px_2px_0_#000] flex items-center gap-2 cursor-pointer"
              @click="close"
            >
              <span class="text-xs font-black uppercase">ABORT</span>
              <span class="text-xl font-black">✖</span>
            </button>
          </div>

          <div class="flex-1 overflow-y-auto relative custom-scrollbar">
            <div class="p-6 md:p-10 relative z-10">
              <TrackForm
                v-if="step === 'form'"
                :is-loading="isLoading"
                @submit-form="generateContract"
              />

              <ContractPreview
                v-else-if="step === 'preview'"
                :pdf-url="pdfUrl"
                :is-loading="isLoading"
                @upload-signed="uploadSignedContract"
              />

              <div
                v-else-if="step === 'success'"
                class="text-center py-12 flex flex-col items-center border-4 border-[#39FF14] bg-black/80"
              >
                <div class="text-[80px] leading-none mb-4 text-[#39FF14]">✔</div>
                <h3 class="text-3xl sm:text-5xl font-black mb-4 uppercase italic">MISSION_COMPLETE</h3>
                <p class="text-gray-400 font-mono text-xs sm:text-sm mb-4 uppercase max-w-md">
                  Один договор на релиз «{{ releaseDraft?.title }}» ({{ releaseDraft?.type }}).
                  Треков в спецификации: {{ releaseDraft?.tracks.length || 0 }}.
                </p>
                <p class="text-gray-600 font-mono text-[10px] mb-10 uppercase">
                  Дальше — загрузка обложки и аудио по треклисту
                </p>
                <button
                  type="button"
                  class="bg-[#39FF14] text-black font-black uppercase text-xl px-10 py-5 border-4 border-black shadow-[10px_10px_0_#fff]"
                  @click="finishAndProceed"
                >
                  &gt;&gt; START_UPLINK
                </button>
              </div>

              <div
                v-if="errorMessage"
                class="mt-8 p-6 bg-[#ff0000] text-black border-4 border-black flex items-start gap-4"
              >
                <span class="text-4xl font-black">[!]</span>
                <div>
                  <p class="text-lg font-black uppercase italic">ERROR</p>
                  <p class="font-mono text-xs uppercase">{{ errorMessage }}</p>
                </div>
              </div>
            </div>
          </div>

          <div class="bg-black border-t-4 border-[#333] p-2 flex justify-between text-[8px] font-mono text-gray-700 uppercase italic shrink-0">
            <span>CONTRACT_SCOPE: RELEASE</span>
            <span>UPLINK: {{ isLoading ? 'ACTIVE' : 'IDLE' }}</span>
          </div>
        </div>
      </div>
    </Transition>
  </Teleport>
</template>

<script lang="ts">
import { defineComponent } from 'vue'
import TrackForm from './TrackForm.vue'
import ContractPreview from './ContractPreview.vue'
import type { ReleaseDraft } from '@/types/release'

export default defineComponent({
  name: 'ContractModal',
  components: { TrackForm, ContractPreview },
  props: {
    isOpen: { type: Boolean, required: true },
  },
  emits: {
    close: () => true,
    success: (payload: { release: ReleaseDraft }) => true,
  },
  data() {
    return {
      step: 'form' as 'form' | 'preview' | 'success',
      isLoading: false,
      errorMessage: '',
      pdfUrl: '',
      releaseDraft: null as ReleaseDraft | null,
    }
  },
  watch: {
    isOpen(val: boolean) {
      if (val) {
        this.step = 'form'
        this.errorMessage = ''
        this.releaseDraft = null
        document.addEventListener('keydown', this.handleEsc)
      } else {
        document.removeEventListener('keydown', this.handleEsc)
      }
    },
  },
  beforeUnmount() {
    document.removeEventListener('keydown', this.handleEsc)
  },
  methods: {
    handleEsc(e: KeyboardEvent) {
      if (e.key === 'Escape' && this.isOpen) this.close()
    },
    close() {
      this.$emit('close')
    },
    finishAndProceed() {
      if (this.releaseDraft) {
        this.$emit('success', { release: this.releaseDraft })
      }
      this.close()
    },
    async generateContract(draft: ReleaseDraft) {
      this.isLoading = true
      this.errorMessage = ''
      this.releaseDraft = draft
      try {
        await new Promise((r) => setTimeout(r, 800))
        this.pdfUrl =
          'https://www.w3.org/WAI/ER/tests/xhtml/testfiles/resources/pdf/dummy.pdf'
        this.step = 'preview'
      } catch (e: unknown) {
        this.errorMessage = e instanceof Error ? e.message : 'Generate failed'
      } finally {
        this.isLoading = false
      }
    },
    async uploadSignedContract(_file: File) {
      this.isLoading = true
      this.errorMessage = ''
      try {
        await new Promise((r) => setTimeout(r, 800))
        this.step = 'success'
      } catch (e: unknown) {
        this.errorMessage = e instanceof Error ? e.message : 'Upload failed'
      } finally {
        this.isLoading = false
      }
    },
  },
})
</script>

<style scoped>
.custom-scrollbar::-webkit-scrollbar {
  width: 10px;
}
.custom-scrollbar::-webkit-scrollbar-track {
  background: #000;
  border-left: 2px solid #222;
}
.custom-scrollbar::-webkit-scrollbar-thumb {
  background: #333;
  border: 2px solid #39ff14;
}
@keyframes real-port-flicker {
  0%,
  100% {
    opacity: 1;
  }
  50% {
    opacity: 0.1;
  }
}
.animate-led {
  animation: real-port-flicker 2s infinite steps(1);
}
.crt-popup-enter-active,
.crt-popup-leave-active {
  transition: all 0.3s steps(6);
}
.crt-popup-enter-from,
.crt-popup-leave-to {
  opacity: 0;
  transform: scale(0.5, 0.01);
}
</style>
