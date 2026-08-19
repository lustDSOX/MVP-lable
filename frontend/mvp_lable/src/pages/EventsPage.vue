<template>
  <section class="min-h-screen py-10 sm:py-16 lg:py-20 px-4 lg:px-10 font-['Impact','Arial_Black',sans-serif] text-white overflow-hidden relative selection:bg-[#ff0000]">
    <div class="max-w-7xl mx-auto relative z-10">
      <div class="mb-10 sm:mb-20 flex flex-col md:flex-row items-start md:items-end justify-between border-b-5 border-[#333] p-4 sm:p-6 border-double gap-4">
        <h1 class="text-4xl sm:text-5xl md:text-7xl lg:text-[140px] leading-none scale-y-110 sm:scale-y-125 uppercase tracking-tight text-white drop-shadow-[3px_3px_0_#39FF14] sm:drop-shadow-[5px_5px_0_#39FF14]">
          EV<span class="text-[#ff0000]">E</span>NTS_
        </h1>
        <div class="bg-[#ff0000] text-black px-4 py-2 font-mono text-xs font-bold animate-pulse shadow-[4px_4px_0_#fff]">
          STATUS: SELLING_OUT_FAST
        </div>
      </div>

      <div class="grid grid-cols-1 gap-6 sm:gap-8 lg:gap-12">
        <div
          v-for="event in events"
          :key="event.id"
          class="group relative bg-[#0a0a0a] border-4 border-[#222] transition-none hover:border-[#39FF14] flex flex-col lg:flex-row shadow-[15px_15px_0_#111] hover:shadow-[15px_15px_0_#39FF14] overflow-hidden"
        >
          <div class="lg:w-48 bg-[#111] border-b-4 lg:border-b-0 lg:border-r-4 border-dashed border-[#333] p-6 flex flex-col items-center justify-center relative group-hover:bg-[#ff0000] transition-none">
            <div class="absolute -top-4 -right-4 w-8 h-8 bg-[#050505] rounded-full border-4 border-[#222] hidden lg:block"></div>
            <div class="absolute -bottom-4 -right-4 w-8 h-8 bg-[#050505] rounded-full border-4 border-[#222] hidden lg:block"></div>
            <div class="text-center group-hover:text-black transition-none">
              <span class="block text-4xl leading-none uppercase italic">{{ dateParts(event.date).day }}</span>
              <span class="block text-xl font-bold border-t-2 border-current mt-2 pt-2">{{ dateParts(event.date).mon }}</span>
              <span class="block text-sm font-mono mt-4 opacity-50">{{ event.time }}</span>
            </div>
          </div>

          <div class="flex-1 p-4 sm:p-6 md:p-8 relative overflow-hidden">
            <h2 class="text-2xl sm:text-4xl uppercase italic mb-2 tracking-tight">{{ event.title }}</h2>
            <p class="font-mono text-xs text-gray-400 uppercase mb-3">{{ event.city }} · {{ event.venue }}</p>
            <p class="font-mono text-sm text-gray-300 normal-case tracking-normal mb-6">{{ event.description }}</p>
            <router-link
              to="/purchase"
              class="inline-flex items-center justify-center min-h-[48px] px-6 bg-[#39FF14] text-black border-4 border-black font-black uppercase text-sm shadow-[4px_4px_0_#ff0000] hover:bg-black hover:text-[#39FF14] hover:border-[#39FF14]"
            >
              Купить билет
            </router-link>
          </div>
        </div>
      </div>

      <p v-if="!events.length" class="font-mono text-[#ff0000] mt-8">NO_EVENTS</p>
    </div>
  </section>
</template>

<script setup lang="ts">
import { computed, onMounted } from 'vue'
import { useCmsStore } from '@/stores/cms'

const cms = useCmsStore()
onMounted(() => cms.hydrate())
const events = computed(() => cms.publishedEvents)

function dateParts(d: string) {
  const parts = (d || '').trim().split(/\s+/)
  return { day: parts[0] || d, mon: parts[1] || '' }
}
</script>
