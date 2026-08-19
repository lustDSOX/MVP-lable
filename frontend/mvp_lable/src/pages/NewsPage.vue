<template>
  <section class="min-h-screen pt-24 sm:pt-32 pb-20 px-4 lg:px-10 font-['Impact','Arial_Black',sans-serif] text-white overflow-hidden relative selection:bg-[#ff0000] selection:text-white">
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

      <div class="relative w-screen left-1/2 -translate-x-1/2 h-10 mb-10 sm:mb-20 flex items-center justify-center overflow-hidden hidden md:flex">
        <div class="absolute inset-0 bg-chain-placeholder bg-repeat-x bg-center bg-size-[auto_300%]"></div>
      </div>

      <div v-if="newsList.length > 0" class="space-y-5 sm:space-y-8 md:space-y-12">
        <NewsItem
          v-for="(news, index) in newsList"
          :key="news.id"
          :id="news.id"
          :index="index + 1"
          :title="news.title"
          :description="news.description"
          :published-at="news.publishedAt"
          :source-link="news.sourceLink"
        />
      </div>

      <div v-else class="bg-[#111] border-4 border-[#ff0000] p-12 text-center shadow-[15px_15px_0_#000]">
        <h2 class="text-4xl font-black text-[#ff0000] uppercase italic">NO_DATA_PACKETS_FOUND</h2>
        <p class="text-gray-500 font-mono mt-4 uppercase">System is waiting for upcoming urban transmissions.</p>
      </div>
    </div>

    <img
      src="@/assets/chrome/chain.png"
      alt=""
      loading="lazy"
      decoding="async"
      class="hidden lg:block absolute h-[250px] rotate-35 -left-20 top-1/3 opacity-20 pointer-events-none select-none mix-blend-screen"
    />
  </section>
</template>

<script setup lang="ts">
import { computed, onMounted } from 'vue'
import NewsItem from '@/components/news/NewsItem.vue'
import { useCmsStore } from '@/stores/cms'

const cms = useCmsStore()
onMounted(() => cms.hydrate())

const newsList = computed(() =>
  cms.publishedNews.map((n) => ({
    id: n.id,
    title: n.title,
    description: n.excerpt || n.body,
    publishedAt: n.date,
    sourceLink: '#',
  })),
)
</script>
