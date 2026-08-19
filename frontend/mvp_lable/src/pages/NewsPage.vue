<template>
  <section class="min-h-screen pt-32 pb-20 px-4 lg:px-10 font-['Impact','Arial_Black',sans-serif] text-white overflow-hidden relative selection:bg-[#ff0000] selection:text-white">
    <div class="max-w-6xl mx-auto relative z-10">
      <div class="flex flex-col md:flex-row justify-between items-end pb-6 relative">
        <div class="relative">
          <h1 class="font-planet h1-metal-textured" data-text="NEWS_LOG">NEWS_LOG</h1>
        </div>
        <div class="hidden lg:block text-right font-mono text-[12px] text-gray-500 uppercase">
          <p>Frequency: 142.06 MHz</p>
          <p>Location: [ REDACTED ]</p>
          <p>Signal: 100% SECURE</p>
        </div>
      </div>

      <div class="relative w-screen left-1/2 -translate-x-1/2 h-10 mb-10 hidden md:flex items-center justify-center overflow-hidden">
        <div class="absolute inset-0 bg-chain-placeholder bg-repeat-x bg-center bg-size-[auto_300%]"></div>
      </div>

      <div v-if="active" class="max-w-4xl mx-auto mb-16">
        <button type="button" class="font-mono text-xs uppercase border-2 border-[#333] px-4 py-2 mb-6 hover:border-[#39FF14]" @click="active = null">
          ← К списку
        </button>
        <article class="y2k-metal p-8 lg:p-12">
          <div class="flex justify-between font-mono text-[10px] text-gray-500 uppercase mb-4">
            <span>SOURCE SOX</span>
            <span>[{{ active.date }}]</span>
          </div>
          <h2 class="text-3xl sm:text-5xl font-black uppercase italic tracking-tighter mb-4">{{ active.title }}</h2>
          <p v-if="active.excerpt" class="text-gray-400 font-mono text-sm mb-6">{{ active.excerpt }}</p>
          <div class="prose-news font-['Inter',sans-serif] text-gray-200 text-base leading-relaxed normal-case font-normal" v-html="mdToHtml(active.body)" />
        </article>
      </div>

      <template v-else>
        <div class="flex flex-col sm:flex-row gap-3 mb-8 font-['Inter',sans-serif]">
          <input
            v-model="search"
            type="search"
            placeholder="Поиск по новостям…"
            class="flex-1 bg-black border-2 border-[#333] px-4 py-3 font-mono text-sm text-white focus:border-[#39FF14] outline-none"
          />
          <select v-model="yearFilter" class="bg-black border-2 border-[#333] px-4 py-3 font-mono text-sm text-white">
            <option value="">Все годы</option>
            <option v-for="y in years" :key="y" :value="y">{{ y }}</option>
          </select>
        </div>

        <div v-if="pageItems.length > 0" class="space-y-12">
          <NewsItem
            v-for="(news, index) in pageItems"
            :key="news.id"
            :id="news.id"
            :index="(page - 1) * pageSize + index + 1"
            :title="news.title"
            :description="news.excerpt || news.body"
            :published-at="news.date"
            @open="openNews(news.id)"
          />
        </div>

        <div v-if="loading" class="flex flex-col items-center justify-center py-20 border-4 border-dashed border-[#222]">
          <div class="w-16 h-16 border-8 border-t-[#39FF14] border-[#111] rounded-full animate-spin mb-4"></div>
          <p class="text-2xl font-black text-[#39FF14] animate-pulse italic uppercase">CONNECTING_TO_SATELLITE...</p>
        </div>

        <div v-if="!loading && filtered.length === 0" class="bg-[#111] border-4 border-[#ff0000] p-12 text-center shadow-[15px_15px_0_#000]">
          <h2 class="text-4xl font-black text-[#ff0000] uppercase italic">NO_DATA_PACKETS_FOUND</h2>
          <p class="text-gray-500 font-mono mt-4 uppercase">System is waiting for upcoming urban transmissions.</p>
        </div>

        <div v-if="totalPages > 1" class="flex flex-wrap justify-center gap-2 mt-12 font-mono text-sm">
          <button type="button" class="px-3 py-2 border-2 border-[#333] disabled:opacity-30" :disabled="page <= 1" @click="page--">←</button>
          <button
            v-for="p in totalPages"
            :key="p"
            type="button"
            class="px-3 py-2 border-2 min-w-[2.5rem]"
            :class="p === page ? 'border-[#39FF14] text-[#39FF14]' : 'border-[#333]'"
            @click="page = p"
          >{{ p }}</button>
          <button type="button" class="px-3 py-2 border-2 border-[#333] disabled:opacity-30" :disabled="page >= totalPages" @click="page++">→</button>
        </div>
      </template>
    </div>

    <img src="@/assets/chrome/chain.png" alt="" class="absolute h-250 rotate-35 -top-28 -left-70 pointer-events-none hidden md:block" />
  </section>
</template>

<script setup lang="ts">
import { computed, onMounted, ref, watch } from 'vue'
import NewsItem from '@/components/news/NewsItem.vue'
import { useCmsStore, type NewsItem as CmsNews } from '@/stores/cms'
import { mdToHtml } from '@/utils/md'

const cms = useCmsStore()
const loading = ref(true)
const search = ref('')
const yearFilter = ref('')
const page = ref(1)
const pageSize = 3
const active = ref<CmsNews | null>(null)

onMounted(() => {
  cms.hydrate()
  loading.value = false
})

const years = computed(() => {
  const set = new Set(cms.publishedNews.map((n) => n.date.slice(0, 4)))
  return [...set].sort().reverse()
})

const filtered = computed(() => {
  let list = cms.publishedNews
  const q = search.value.trim().toLowerCase()
  if (q) {
    list = list.filter(
      (n) =>
        n.title.toLowerCase().includes(q) ||
        n.excerpt.toLowerCase().includes(q) ||
        n.body.toLowerCase().includes(q),
    )
  }
  if (yearFilter.value) list = list.filter((n) => n.date.startsWith(yearFilter.value))
  return list
})

const totalPages = computed(() => Math.max(1, Math.ceil(filtered.value.length / pageSize)))
const pageItems = computed(() => {
  const start = (page.value - 1) * pageSize
  return filtered.value.slice(start, start + pageSize)
})

watch([search, yearFilter], () => {
  page.value = 1
  active.value = null
})

function openNews(id: string) {
  const n = cms.publishedNews.find((x) => x.id === id)
  if (n) {
    active.value = n
    window.scrollTo({ top: 0, behavior: 'smooth' })
  }
}
</script>

<style scoped>
.bg-chain-placeholder {
  background-image: url('@/assets/chrome/chain_bg.png');
}
.y2k-metal {
  background: linear-gradient(145deg, #1a1a1a, #0a0a0a);
  border: 4px solid #333;
  box-shadow: 8px 8px 0 #000;
}
.prose-news :deep(h1),
.prose-news :deep(h2),
.prose-news :deep(h3) {
  font-family: Impact, 'Arial Black', sans-serif;
  font-weight: 900;
  text-transform: uppercase;
  margin: 0.75em 0 0.35em;
  color: #fff;
}
.prose-news :deep(a) {
  color: #39ff14;
}
.prose-news :deep(img) {
  max-width: 100%;
  border: 2px solid #333;
  margin: 1rem 0;
}
</style>
