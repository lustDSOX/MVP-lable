<template>
  <section class="min-h-screen relative overflow-hidden bg-black text-white font-['Impact','Arial_Black',sans-serif] selection:bg-[#39FF14] selection:text-black">
    
    <div class="absolute inset-0 y2k-bg-grid opacity-40 pointer-events-none"></div>
    <div class="absolute inset-0 crt-noise opacity-[0.07] pointer-events-none mix-blend-overlay"></div>

    <div class="relative z-10 max-w-6xl mx-auto px-4 sm:px-6 pt-24 sm:pt-28 pb-16">
      
      <div class="mb-10 sm:mb-14 border-b-4 border-[#39FF14] pb-4 inline-block max-w-full">
        <h1 class="text-4xl sm:text-5xl md:text-6xl font-black uppercase italic leading-none text-white drop-shadow-[4px_4px_0_#39FF14]">
          ARTIST_GUIDES
        </h1>
        <p class="font-mono text-[10px] sm:text-xs text-gray-500 mt-2 tracking-widest uppercase">
          protocol_for_unsigned // class_tickets_docs
        </p>
      </div>

      <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4 sm:gap-6">
        <router-link
          v-for="g in guides"
          :key="g.id"
          :to="`/guides/${g.id}`"
          class="group block border-4 border-[#222] bg-[#0a0a0a] p-4 sm:p-6 hover:border-[#39FF14] hover:shadow-[6px_6px_0_#39FF14] transition-none min-h-[160px]"
        >
          <div class="flex items-center gap-2 mb-3 font-mono text-[10px] text-[#39FF14]">
            <span class="bg-black border border-[#39FF14] px-1">0{{ g.id }}</span>
            <span class="text-gray-600">{{ g.level || 'GUIDE' }}</span>
          </div>
          <h2 class="text-xl sm:text-2xl font-black uppercase leading-tight mb-3 group-hover:text-[#39FF14]">
            {{ g.title }}
          </h2>
          <p class="font-mono text-xs sm:text-sm text-gray-500 leading-relaxed line-clamp-3">
            {{ g.description }}
          </p>
          <span class="inline-block mt-4 text-xs font-black text-black bg-[#39FF14] px-2 py-1 uppercase group-hover:bg-white">
            OPEN →
          </span>
        </router-link>
      </div>

      <div class="mt-12 border-2 border-[#222] bg-[#111] p-4 sm:p-6 flex flex-col sm:flex-row gap-4 items-start sm:items-center justify-between">
        <div class="font-mono text-[10px] sm:text-xs text-gray-500 uppercase leading-relaxed">
          <span class="text-[#ff0000] font-bold block mt-1">.SOX IS NOT RESPONSIBLE FOR THE ENTITIES YOU SUMMON.</span>
        </div>
        <div class="shrink-0 flex flex-col items-center">
          <span class="font-mono text-[8px] tracking-widest text-[#666]">SCAN_AT_YOUR_OWN_RISK</span>
        </div>
      </div>
    </div>
  </section>
</template>

<style scoped>
.y2k-bg-grid {
  background-size: 20px 20px;
  background-image: radial-gradient(circle, #222 1px, transparent 1px);
}
.crt-noise {
  background-image: url('data:image/svg+xml;utf8,%3Csvg viewBox="0 0 200 200" xmlns="http://www.w3.org/2000/svg"%3E%3Cfilter id="noiseFilter"%3E%3CfeTurbulence type="fractalNoise" baseFrequency="0.9" numOctaves="3" stitchTiles="stitch"/%3E%3C/filter%3E%3Crect width="100%25" height="100%25" filter="url(%23noiseFilter)"/%3E%3C/svg%3E');
}
</style>

<script lang="ts">
import { defineComponent } from 'vue'
import { guides } from '@/data/guides'

export default defineComponent({
  name: 'GuidesPage',
  data() {
    return {
      guides,
    }
  },
})
</script>
