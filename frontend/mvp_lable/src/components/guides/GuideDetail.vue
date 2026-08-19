<template>
  <section class="min-h-screen pt-32 pb-20 px-4 lg:px-10 text-white bg-black font-['Inter',sans-serif]">
    <div class="max-w-3xl mx-auto">
      <router-link to="/guides" class="font-mono text-xs uppercase border-2 border-[#333] px-4 py-2 inline-block mb-8 hover:border-[#39FF14]">
        ← К гайдам
      </router-link>

      <div v-if="guide" class="border-4 border-[#333] p-6 sm:p-10 bg-[#0a0a0a]">
        <p class="font-mono text-[10px] text-[#39FF14] uppercase mb-2">{{ guide.category }} · {{ guide.status }}</p>
        <h1 class="text-3xl sm:text-5xl font-black uppercase tracking-tighter mb-4">{{ guide.title }}</h1>
        <p v-if="guide.excerpt" class="text-gray-400 font-mono text-sm mb-8">{{ guide.excerpt }}</p>
        <div class="prose-guide text-gray-200 leading-relaxed" v-html="mdToHtml(guide.body)" />
      </div>

      <div v-else class="border-4 border-[#ff0000] p-10 text-center">
        <p class="font-black uppercase text-[#ff0000] text-2xl">GUIDE_NOT_FOUND</p>
        <router-link to="/guides" class="font-mono text-sm text-[#39FF14] mt-4 inline-block">← back</router-link>
      </div>
    </div>
  </section>
</template>

<script setup lang="ts">
import { computed, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import { useCmsStore } from '@/stores/cms'
import { mdToHtml } from '@/utils/md'

const route = useRoute()
const cms = useCmsStore()
onMounted(() => cms.hydrate())

const guide = computed(() => {
  const id = String(route.params.id)
  return cms.publishedGuides.find((g) => g.id === id) || cms.guides.find((g) => g.id === id) || null
})
</script>

<style scoped>
.prose-guide :deep(h1),
.prose-guide :deep(h2),
.prose-guide :deep(h3) {
  font-weight: 900;
  text-transform: uppercase;
  margin: 1em 0 0.4em;
  color: #fff;
}
.prose-guide :deep(a) {
  color: #39ff14;
}
.prose-guide :deep(img) {
  max-width: 100%;
  border: 2px solid #333;
  margin: 1rem 0;
}
.prose-guide :deep(blockquote) {
  border-left: 4px solid #39ff14;
  padding-left: 1rem;
  color: #9ca3af;
}
</style>
