<template>
  <div class="min-h-screen pt-20 sm:pt-24 px-3 sm:px-4 pb-16 text-white font-['Impact','Arial_Black',sans-serif]">
    <div class="max-w-5xl mx-auto">
      <div class="flex flex-wrap items-end justify-between gap-4 mb-10 border-b-4 border-[#222] pb-6">
        <h1 class="text-5xl sm:text-7xl uppercase italic tracking-tighter leading-none">
          LIVE<span class="text-[#ff0000]">_</span>EVENTS
        </h1>
        <span class="font-mono text-xs text-[#39FF14]">{{ list.length }} PUBLISHED</span>
      </div>

      <div v-if="list.length" class="space-y-6">
        <article
          v-for="event in list"
          :key="event.id"
          class="group flex flex-col lg:flex-row border-4 border-[#222] bg-[#0a0a0a] shadow-[12px_12px_0_#111] hover:shadow-[12px_12px_0_#39FF14] overflow-hidden"
        >
          <div class="lg:w-44 bg-[#111] border-b-4 lg:border-b-0 lg:border-r-4 border-dashed border-[#333] p-6 flex flex-col items-center justify-center group-hover:bg-[#ff0000] group-hover:text-black transition-none">
            <span class="block text-3xl uppercase italic">{{ event.date }}</span>
            <span class="block text-sm font-mono mt-2 opacity-70">{{ event.time }}</span>
          </div>
          <div class="flex-1 p-5 sm:p-8">
            <h2 class="text-2xl sm:text-4xl uppercase italic mb-2">{{ event.title }}</h2>
            <p class="font-mono text-xs text-gray-400 uppercase mb-3">{{ event.city }} · {{ event.venue }}</p>
            <p class="font-mono text-sm text-gray-300 normal-case tracking-normal">{{ event.description }}</p>
          </div>
        </article>
      </div>
      <p v-else class="font-mono text-[#ff0000]">NO_EVENTS</p>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed, onMounted } from 'vue'
import { useCmsStore } from '@/stores/cms'

const cms = useCmsStore()
onMounted(() => cms.hydrate())
const list = computed(() => cms.publishedEvents)
</script>
