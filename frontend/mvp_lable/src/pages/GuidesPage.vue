<template>
  <section class="min-h-screen pt-32 pb-20 px-4 lg:px-10 font-['Inter',sans-serif] text-white overflow-hidden relative selection:bg-[#ff0000] selection:text-white bg-black">
    <div class="absolute inset-0 pointer-events-none z-0 opacity-[0.15]"></div>
    <div class="max-w-7xl mx-auto relative z-10">
      <div class="mb-10 flex flex-col items-start border-b-4 border-[#222] pb-6 relative">
        <div class="absolute top-0 right-0 bg-[#ff0000] text-white font-['JetBrains_Mono',monospace] text-xs font-bold px-3 py-1 uppercase tracking-widest rotate-2">
          System_Breach
        </div>
        <h1 class="variant-corrupted-brutal m-0 text-4xl sm:text-6xl font-black uppercase tracking-tighter" data-text="ARTIST_GUIDES">
          ARTIST_GUIDES
        </h1>
      </div>

      <div class="flex flex-col sm:flex-row gap-3 mb-8">
        <input
          v-model="search"
          type="search"
          placeholder="Поиск гайдов…"
          class="flex-1 bg-black border-2 border-[#333] px-4 py-3 font-mono text-sm focus:border-[#39FF14] outline-none"
        />
        <select v-model="catFilter" class="bg-black border-2 border-[#333] px-4 py-3 font-mono text-sm">
          <option value="">Все категории</option>
          <option v-for="c in categories" :key="c" :value="c">{{ c }}</option>
        </select>
      </div>

      <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 border-t-2 border-l-2 border-[#333] bg-black">
        <router-link
          v-for="(guide, index) in filtered"
          :key="guide.id"
          :to="{ name: 'GuideDetail', params: { id: guide.id } }"
          class="group relative p-8 overflow-hidden cursor-crosshair min-h-[16rem] flex flex-col border-b-2 border-r-2 border-[#333] hover:bg-[#050505]"
        >
          <div class="relative z-10 h-full flex flex-col justify-between">
            <div class="flex justify-between items-start mb-4">
              <span class="text-5xl font-black text-white leading-none tracking-tighter group-hover:text-[#ff0000]">
                {{ String(index + 1).padStart(2, '0') }}
              </span>
              <div class="border border-[#444] px-2 py-1 font-mono font-bold text-[10px] uppercase text-[#666] group-hover:border-[#39FF14] group-hover:text-[#39FF14]">
                {{ guide.category }}
              </div>
            </div>
            <div>
              <h2 class="text-xl font-black uppercase tracking-tight mb-2 group-hover:text-[#39FF14]">{{ guide.title }}</h2>
              <p class="font-mono text-xs text-gray-500 line-clamp-3">{{ guide.excerpt }}</p>
            </div>
          </div>
        </router-link>
      </div>

      <p v-if="!filtered.length" class="font-mono text-gray-600 mt-8 text-center">NO_GUIDES</p>
    </div>
  </section>
</template>

<script setup lang="ts">
import { computed, onMounted, ref } from 'vue'
import { useCmsStore } from '@/stores/cms'

const cms = useCmsStore()
const search = ref('')
const catFilter = ref('')

onMounted(() => cms.hydrate())

const categories = computed(() => {
  const s = new Set(cms.publishedGuides.map((g) => g.category).filter(Boolean))
  return [...s].sort()
})

const filtered = computed(() => {
  let list = cms.publishedGuides
  const q = search.value.trim().toLowerCase()
  if (q) {
    list = list.filter(
      (g) =>
        g.title.toLowerCase().includes(q) ||
        g.excerpt.toLowerCase().includes(q) ||
        g.body.toLowerCase().includes(q),
    )
  }
  if (catFilter.value) list = list.filter((g) => g.category === catFilter.value)
  return list
})
</script>
