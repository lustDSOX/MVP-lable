<template>
  <section class="min-h-screen px-4 lg:px-32 py-20 pb-12 font-['Impact','Arial_Black',sans-serif] selection:bg-[#39FF14] selection:text-black relative overflow-hidden bg-[#050805]">

    <div class="absolute inset-0 z-100 pointer-events-none select-none overflow-hidden">

      <div class="absolute inset-0 bg-[url('https://www.transparenttextures.com/patterns/stardust.png')] opacity-20 mix-blend-screen animate-noise transform-gpu"></div>
      <div class="absolute inset-0 bg-[radial-gradient(circle_at_center,transparent_10%,rgba(0,0,0,0.4)_80%,rgba(0,0,0,0.9)_90%,#000_100%)] z-10 transform-gpu"></div>
      <div class="absolute inset-0 bg-[linear-gradient(rgba(18,16,16,0)_50%,rgba(57,255,20,0.02)_100%)] bg-size-[100%_8px] animate-[scan-roll_20s_linear_infinite] transform-gpu"></div>
      <div class="fixed inset-0 z-40 pointer-events-none bg-[radial-gradient(circle,transparent_50%,rgba(0,0,0,0.5)_80%,rgba(0,0,0,1)_100%)] transform-gpu"></div>

      <div class="absolute top-20 right-30 font-mono text-[#39FF14] text-xs opacity-70 pointer-events-none select-none">
        <div class="flex items-center gap-2">
          <div class="w-2 h-2 bg-[#39FF14] rounded-full animate-pulse"></div>
          PLAY 00:44
        </div>
        <div class="text-right">SP</div>
      </div>

      <div class="absolute inset-0 pointer-events-none z-40 overflow-hidden">
        <div class="absolute w-full h-32 bg-white/5 blur-3xl animate-[tracking-line_12s_linear_infinite]"></div>
      </div>

      <div class="absolute left-15 top-1/2 -translate-y-1/2 flex flex-col gap-4 opacity-40 font-mono text-[8px] text-[#39FF14] lg:flex">
        <span v-for="n in 5" :key="n" class="border-t border-[#39FF14] w-2">{{ 100 - n * 20 }}%</span>
      </div>

    </div>

<div class="fixed inset-0 pointer-events-none z-50 shadow-[inset_0_0_150px_rgba(0,0,0,0.8)]"></div>

    <div class="max-w-7xl mx-auto relative z-10 transform scale-y-[1.02] scale-x-[0.98] rounded-[100px/40px]">
      
      <!-- АГРЕССИВНЫЙ ЗАГОЛОВОК -->
      <div class="mb-16 border-b-8 border-[#39FF14] pb-4 inline-block transform">
        <h1 class="variant-vhs py-0 mb-10" data-text="CASE_FILES">
         CASE_FILES
        </h1>
        <div class="text-[10px] font-mono text-[#ff0000] mt-2 animate-pulse tracking-[0.5em]">
          SCANNING_DATABASE... 100% COMPLETE
        </div>
      </div>

      <!-- СЕТКА: ЖЕСТКИЕ ПАНЕЛИ (Gap-0 для эффекта монолитности) -->
      <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-0 border-4 border-[#222] bg-[#222]">
        <CaseItem
          v-for="caseItem in cases"
          :key="caseItem.id"
          :id="caseItem.id"
          :title="caseItem.title"
          :description="caseItem.description"
          :logo="caseItem.logo"
          @open="openModal(caseItem)"
        />
      </div>
    </div>


    <Transition name="glitch-fade">
      <CaseDetail 
        v-if="activeCase" 
        :caseData="activeCase" 
        @close="activeCase = null" 
      />
    </Transition>
  </section>
</template>

<script lang="ts">
import { defineComponent } from 'vue'
import CaseItem from '@/components/cases/CaseItem.vue'
import CaseDetail from '@/components/cases/CaseDetail.vue';

export default defineComponent({
  name: 'CasesPage',

  components: {
    CaseItem,
    CaseDetail
  },

  data() {
    return {
      cases: [
        {
          id: 1,
          title: 'Streetflow Project',
          description: 'Первый цифровой альбом, собравший 10000 билетов за месяц. Уличные коллабы, стрит‑арт визуал, релиз в 3 городах.',
          logo: '/assets/cases/streetflow.png',
        },
        {
          id: 2,
          title: 'Neon Freestyle',
          description: 'Мини‑тур из 5 лайв‑сейшенов с фреш‑треками каждый день. Каждый вход — отдельный билет‑класс.',
          logo: '/assets/cases/neonfreestyle.png',
        },
        {
          id: 3,
          title: 'Underground Mixtape',
          description: 'Сбор локальных фри‑стайлеров: 12 артистов, один пакет билетов, 300% рост подписчиков за 2 недели.',
          logo: '/assets/cases/undergroundmixtape.png',
        },
      ] as CaseItemData[],

      activeCase: null as CaseItemData | null,
    }
  },

  methods: {
    openModal(selectedCase: CaseItemData) {
      this.activeCase = selectedCase;
    }
  }

})

interface CaseItemData {
  id: number
  title: string
  description: string
  logo: string
}
</script>