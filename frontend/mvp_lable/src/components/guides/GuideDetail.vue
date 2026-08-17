<template>
  <section class="min-h-screen px-4 sm:px-6 pb-16 pt-20 sm:pt-24 font-['Impact','Arial_Black',sans-serif] text-white relative overflow-x-hidden">
    <div class="max-w-3xl mx-auto relative z-10">
      <!-- Back -->
      <router-link
        to="/guides"
        class="inline-flex items-center gap-2 min-h-[44px] px-3 py-2 mb-6 border-2 border-[#39FF14] bg-black text-[#39FF14] text-sm sm:text-base font-black uppercase hover:bg-[#39FF14] hover:text-black active:translate-x-0.5 active:translate-y-0.5"
      >
        ← BACK_TO_GUIDES
      </router-link>

      <template v-if="guide">
        <!-- Meta bar -->
        <div class="flex flex-wrap gap-2 mb-4 font-mono text-[10px] sm:text-xs tracking-wider">
          <span class="bg-[#39FF14] text-black px-2 py-1 font-bold">ID_{{ String(guide.id).padStart(2, '0') }}</span>
          <span v-if="guide.level" class="border border-[#333] text-gray-400 px-2 py-1">{{ guide.level }}</span>
          <span v-if="guide.duration" class="border border-[#333] text-gray-400 px-2 py-1">{{ guide.duration }}</span>
          <span
            v-for="tag in guide.tags || []"
            :key="tag"
            class="border border-[#222] text-[#39FF14]/80 px-2 py-1"
          >#{{ tag }}</span>
        </div>

        <!-- Title -->
        <h1 class="text-3xl sm:text-4xl md:text-5xl font-black uppercase italic leading-[1.05] mb-6 text-white drop-shadow-[3px_3px_0_#39FF14]">
          {{ guide.title }}
        </h1>

        <div class="h-1 w-full bg-[#39FF14] mb-8 shadow-[0_0_12px_#39FF14]"></div>

        <!-- Body panel -->
        <article class="border-4 border-black bg-[#0a0a0a] shadow-[8px_8px_0_#222] p-4 sm:p-8 relative">
          <div class="absolute top-0 right-0 bg-[#ff0000] text-black text-[10px] font-mono px-2 py-0.5 font-bold">
            CLASSIFIED_GUIDE
          </div>
          <p class="font-mono text-sm sm:text-base text-gray-300 leading-relaxed whitespace-pre-line">
            {{ guide.content }}
          </p>
        </article>

        <!-- Steps hint -->
        <div class="mt-8 border-2 border-[#333] bg-[#111] p-4 sm:p-6">
          <h2 class="text-lg sm:text-xl font-black text-[#39FF14] uppercase mb-3">NEXT_ACTIONS</h2>
          <ol class="font-mono text-xs sm:text-sm text-gray-400 space-y-2 list-decimal list-inside">
            <li>Прочитай материал до конца</li>
            <li>Примени 1 пункт на ближайшей сессии</li>
            <li>Залей черновик через кабинет артиста</li>
          </ol>
        </div>

        <!-- CTA -->
        <div class="mt-8 flex flex-col sm:flex-row gap-3">
          <router-link
            to="/login"
            class="flex-1 text-center min-h-[48px] flex items-center justify-center bg-[#39FF14] text-black border-4 border-black font-black text-lg uppercase shadow-[4px_4px_0_#ff0000] hover:bg-black hover:text-[#39FF14] hover:border-[#39FF14]"
          >
            OPEN_CABINET
          </router-link>
          <router-link
            to="/guides"
            class="flex-1 text-center min-h-[48px] flex items-center justify-center bg-black text-[#39FF14] border-4 border-[#39FF14] font-black text-lg uppercase hover:bg-[#39FF14] hover:text-black"
          >
            ALL_GUIDES
          </router-link>
        </div>

        <p class="mt-8 font-mono text-[9px] text-gray-600 text-center uppercase tracking-widest">
          CLASS TICKETS · materials under artist agreement
        </p>
      </template>

      <div v-else class="border-4 border-[#ff0000] bg-[#111] p-8 text-center shadow-[8px_8px_0_#000]">
        <h2 class="text-2xl sm:text-3xl font-black text-[#ff0000] uppercase italic mb-3">GUIDE_NOT_FOUND</h2>
        <p class="font-mono text-gray-500 text-sm mb-6">Packet missing or id invalid.</p>
        <router-link to="/guides" class="text-[#39FF14] font-bold underline">← guides index</router-link>
      </div>
    </div>
  </section>
</template>

<script lang="ts">
import { defineComponent } from 'vue'
import { getGuideById, type GuideItem } from '@/data/guides'

export default defineComponent({
  name: 'GuideDetail',
  props: {
    id: { type: String, required: true },
  },
  computed: {
    guide(): GuideItem | undefined {
      return getGuideById(this.id)
    },
  },
})
</script>
