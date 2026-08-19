<template>
  <div class="min-h-screen pt-20 sm:pt-24 px-3 sm:px-4 pb-12 text-white relative">
    <div class="max-w-4xl mx-auto relative z-10">
      <header class="mb-8">
        <h1 class="h1-metal-textured text-4xl sm:text-6xl" data-text="NEWS_LOG">NEWS_LOG</h1>
        <p class="font-mono text-[10px] text-gray-500 uppercase mt-2">Published only · CMS mock</p>
      </header>
      <div v-if="list.length" class="space-y-5 sm:space-y-8">
        <NewsItem
          v-for="news in list"
          :key="news.id"
          :id="news.id"
          :title="news.title"
          :description="news.description"
          :published-at="news.publishedAt"
          :source-link="news.sourceLink"
        />
      </div>
      <div v-else class="bg-[#111] border-4 border-[#ff0000] p-12 text-center font-mono">NO_NEWS</div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed, onMounted } from 'vue'
import NewsItem from '@/components/news/NewsItem.vue'
import { useCmsStore } from '@/stores/cms'

const cms = useCmsStore()
onMounted(() => cms.hydrate())

const list = computed(() =>
  cms.publishedNews.map((n) => ({
    id: n.id,
    title: n.title,
    description: n.excerpt || n.body,
    publishedAt: n.date,
    sourceLink: '#',
  })),
)
</script>
