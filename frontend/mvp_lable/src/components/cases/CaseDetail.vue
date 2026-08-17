<template>
  <Teleport to="body">
  <!-- BACKDROP — teleported so Header (z-30) cannot cover close btn -->
  <div 
    @click.self="$emit('close')"
    class="fixed inset-0 z-[200] flex items-end sm:items-center justify-center p-0 sm:p-4 font-['VT323',monospace] text-white overflow-hidden selection:bg-[#39FF14] selection:text-black"
  >
    <div class="absolute inset-0 bg-black/70 backdrop-blur-sm z-0"></div>
    <div class="absolute inset-0 bg-[url('https://www.transparenttextures.com/patterns/stardust.png')] opacity-30 mix-blend-color-dodge pointer-events-none z-0 hidden sm:block"></div>
    
    <div 
      class="relative z-10 w-full sm:max-w-5xl h-[100dvh] sm:h-auto max-h-[100dvh] sm:max-h-[90vh] bg-black/95 sm:bg-black/90 border-0 sm:border-2 border-[#39FF14]/50 flex flex-col 
             shadow-none sm:shadow-[0_0_25px_5px_rgba(57,255,20,0.2)] rounded-none"
    >
      <div class="absolute inset-0 bg-[linear-gradient(rgba(18,16,16,0)_50%,rgba(0,0,0,0.4)_50%)] bg-size-[100%_4px] pointer-events-none z-20 hidden sm:block"></div>

      <div class="bg-[#39FF14] p-2 text-black flex justify-between items-center shrink-0 border-b-2 border-black relative z-[210]">
        <span class="text-base sm:text-xl px-2 tracking-wider truncate">
          SYSTEM_LOG: DOSSIER_00{{ caseData.id }}
        </span>
        <button 
          type="button"
          @click.stop="$emit('close')"
          class="relative z-[210] w-11 h-11 sm:w-10 sm:h-10 flex items-center justify-center bg-black text-white border-2 border-black text-3xl font-black leading-none hover:bg-[#ff0000] hover:border-[#ff0000] active:scale-95 shrink-0"
          aria-label="Close"
        >
          ×
        </button>
      </div>

      <div class="grid grid-cols-1 lg:grid-cols-12 overflow-y-auto flex-1 relative z-30">
        <div class="lg:col-span-4 border-b-2 lg:border-b-0 lg:border-r-2 border-[#39FF14]/30 p-4 sm:p-6 flex flex-col items-center justify-center bg-black/50">
          <div class="w-full max-w-xs sm:max-w-none aspect-square bg-black shadow-[inset_0_0_20px_rgba(0,0,0,0.8)] border border-[#222] flex items-center justify-center p-4 sm:p-6">
             <img :src="caseData.logo" alt="Case Logo" class="w-full h-full object-contain filter-vhs" />
          </div>
        </div>

        <div class="lg:col-span-8 p-4 sm:p-6 md:p-8 flex flex-col">
          <h2 class="text-2xl sm:text-5xl md:text-6xl text-[#39FF14] mb-4 sm:mb-6 font-black leading-tight case-title">
            {{ caseData.title }}
          </h2>
          
          <div class="mb-6 sm:mb-8">
            <p class="text-base sm:text-xl text-white/90 leading-relaxed tracking-wide case-body">
              {{ caseData.description }}
            </p>
          </div>

          <div class="mt-auto pt-6 border-t border-[#39FF14]/30">
            <div class="h-6 w-full border border-[#39FF14]/50 flex mb-4">
              <div v-for="n in 15" :key="n" class="h-full w-full border-r border-black/50 bg-[#39FF14]/80"></div>
            </div>

            <ul class="grid grid-cols-1 sm:grid-cols-2 gap-x-6 gap-y-2">
              <li v-for="res in [
                  'TICKETS: 10K+', 
                  'GROWTH: 300%', 
                  'SESSIONS: 12', 
                  'ACCESS: GRANTED'
                ]" :key="res" class="flex items-center gap-2 text-base sm:text-lg">
                <div class="w-2 h-2 bg-[#ff0000] shrink-0"></div>
                <span class="case-stat">{{ res }}</span>
              </li>
            </ul>
          </div>

        </div>
      </div>
    </div>
  </div>
  </Teleport>
</template>

<script lang="ts">
import { defineComponent, type PropType } from 'vue'

export default defineComponent({
  name: 'CaseModal',
  props: {
    caseData: {
      type: Object as PropType<{ id: number; title: string; description: string; logo: string }>,
      required: true
    }
  },
  emits: ['close'],
  mounted() {
    document.body.style.overflow = 'hidden'
    const onKey = (e: KeyboardEvent) => {
      if (e.key === 'Escape') this.$emit('close')
    }
    ;(this as any)._onKey = onKey
    window.addEventListener('keydown', onKey)
  },
  unmounted() {
    document.body.style.overflow = 'auto'
    const onKey = (this as any)._onKey
    if (onKey) window.removeEventListener('keydown', onKey)
  }
})
</script>

<style scoped>
.bg-size-\[100\%_4px\] {
  background-size: 100% 4px;
}

/* Readable solid text — no glitch jitter */
.case-title {
  text-shadow: 0 0 8px rgba(57, 255, 20, 0.35);
}
.case-body {
  text-shadow: none;
}
.case-stat {
  color: #39FF14;
  text-shadow: none;
}

.filter-vhs {
  filter: grayscale(40%) contrast(1.2) brightness(0.9) drop-shadow(0 0 5px rgba(57, 255, 20, 0.3));
}

@media (min-width: 640px) {
  .case-title {
    position: relative;
    color: rgba(57, 255, 20, 0.95);
  }
}

@media (prefers-reduced-motion: reduce) {
  .animate-window-flicker {
    animation: none !important;
  }
}
</style>
