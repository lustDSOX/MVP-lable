<template>
  <div class="group relative max-w-4xl mx-auto mb-6 sm:mb-10 md:mb-16">
    
    <!-- Chrome decor — desktop only -->
    <div class="hidden md:block absolute -top-1/7 -right-70 w-2/3 z-10 pointer-events-none -rotate-12">
      <img src="@/assets/chrome/t_chrome.webp" 
           loading="lazy"
           decoding="async"
           class="sigil-metal w-full h-full object-contain rotate-0" 
           alt="">
    </div>

    <div class="hidden md:block absolute -bottom-1/12 -left-1/5 w-1/2 z-10 pointer-events-none">
      <img src="@/assets/chrome/b_chrome.webp" 
           loading="lazy"
           decoding="async"
           class="sigil-metal w-full h-full object-contain" 
           alt="">
    </div>

    <div class="y2k-metal news-card p-4 sm:p-6 md:p-10 lg:p-16">

      <div class="relative z-20">
        
        <div class="flex items-center justify-between gap-2 mb-4 sm:mb-6 md:mb-10">
          <div class="flex items-center gap-2 sm:gap-4 text-[10px] sm:text-sm font-mono tracking-[0.2em] sm:tracking-[0.4em] uppercase text-engraved-light">
            SOURCE SOX
          </div>
          <div class="text-[10px] sm:text-sm font-mono text-engraved-light uppercase tracking-[0.15em] sm:tracking-[0.2em] shrink-0">
            [{{ publishedAt }}]
          </div>
        </div>

        <h2 class="text-xl sm:text-3xl md:text-6xl font-cindie uppercase italic tracking-tighter leading-tight sm:leading-none mb-3 sm:mb-6 md:mb-8 text-engraved">
          {{ title }}
        </h2>

        <p class="text-engraved-light font-montserrat leading-snug sm:leading-relaxed max-w-2xl mb-4 sm:mb-8 md:mb-12 text-sm sm:text-lg md:text-2xl">
          {{ description }}
        </p>

        <div class="flex justify-start">
          <a :href="sourceLink" target="_blank"
             class="group/link flex items-center gap-3 sm:gap-6 text-sm sm:text-xl uppercase
                    text-engraved tracking-widest transition-all duration-300 min-h-[44px]">
            <span class="w-8 sm:w-12 h-0.5 bg-black/80 shadow-[0_1px_0_rgba(255,255,255,0.4)] 
                         group-hover/link:w-16 sm:group-hover/link:w-24 group-hover:bg-white transition-all duration-500"></span>
            Access Terminal
          </a>
        </div>
      </div>

      <div class="absolute right-3 bottom-2 sm:right-6 sm:bottom-6 font-mono text-[8px] sm:text-[10px] tracking-widest text-engraved-light opacity-60">
        LOG_ID: 00{{ id }} / SECTOR_01
      </div>

    </div>
  </div>
</template>

<style scoped>
/* Mobile: always "lit" — no hover needed */
@media (max-width: 767px) {
  .news-card :deep(.text-engraved),
  .group .text-engraved {
    color: #ffffff !important;
    text-shadow:
      -1px -1px 1px rgba(0, 0, 0, 0.9),
      0 0 12px rgba(255, 255, 255, 0.25);
  }
  .news-card :deep(.text-engraved-light),
  .group .text-engraved-light {
    color: #e4e4e7 !important;
  }
  .news-card.y2k-metal {
    box-shadow:
      inset 2px 2px 5px rgba(255, 255, 255, 0.45),
      inset -3px -3px 6px rgba(0, 0, 0, 0.9),
      0 0 18px rgba(57, 255, 20, 0.2),
      8px 8px 0 rgba(0, 0, 0, 0.85) !important;
  }
  .news-card.y2k-metal::before {
    filter: contrast(1.05) brightness(0.85) saturate(0.5) !important;
  }
}
</style>

<script lang="ts">
import { defineComponent } from 'vue'
import type { PropType } from 'vue'

export default defineComponent({
  name: 'NewsItem',
  props: {
    id: {
      type: Number as PropType<number>,
      required: true,
    },
    title: {
      type: String as PropType<string>,
      required: true,
    },
    description: {
      type: String as PropType<string>,
      required: true,
    },
    publishedAt: {
      type: String as PropType<string>,
      required: true,
    },
    sourceLink: {
      type: String as PropType<string | undefined>,
    },
  },
  methods: {
    formatDate(dateStr: string) {
      const date = new Date(dateStr)
      const day = String(date.getDate()).padStart(2, '0')
      const month = String(date.getMonth() + 1).padStart(2, '0')
      const year = date.getFullYear()
      return `${day}.${month}.${year}`
    },
  },
})
</script>
