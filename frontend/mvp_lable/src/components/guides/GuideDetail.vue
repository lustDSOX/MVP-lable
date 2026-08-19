<template>
  <section class="min-h-screen pt-24 sm:pt-28 px-4 pb-16 text-white">
    <div class="max-w-3xl mx-auto">
      <router-link
        to="/guides"
        class="font-mono text-xs text-gray-500 uppercase hover:text-[#39FF14] mb-6 inline-block"
      >
        ← guides
      </router-link>

      <template v-if="guide">
        <div class="flex flex-wrap gap-2 mb-4 font-mono text-[10px] sm:text-xs tracking-wider">
          <span class="bg-[#39FF14] text-black px-2 py-1 font-bold">ID_{{ String(guide.id).padStart(2, '0') }}</span>
          <span v-if="guide.level" class="border border-[#333] text-gray-400 px-2 py-1">{{ guide.level }}</span>
          <span v-if="guide.duration" class="border border-[#333] text-gray-400 px-2 py-1">{{ guide.duration }}</span>
          <span
            v-for="tag in guide.tags || []"
            :key="tag"
            class="border border-[#333] text-gray-500 px-2 py-1"
          >{{ tag }}</span>
        </div>

        <h1 class="text-3xl sm:text-5xl font-black uppercase italic tracking-tight mb-6">
          {{ guide.title }}
        </h1>

        <div class="prose-invert font-mono text-sm text-gray-300 space-y-4 leading-relaxed">
          <p class="whitespace-pre-wrap">{{ guide.content }}</p>
        </div>

        <div v-if="guide.steps?.length" class="mt-8 space-y-3">
          <h2 class="font-mono text-xs text-[#39FF14] uppercase">Steps</h2>
          <ol class="list-decimal list-inside space-y-2 font-mono text-sm text-gray-300">
            <li v-for="(s, i) in guide.steps" :key="i">{{ s }}</li>
          </ol>
        </div>

        <div class="mt-8 flex flex-col sm:flex-row gap-3">
          <router-link
            :to="cabinetPath"
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

      <template v-else>
        <p class="font-mono text-[#ff0000]">Guide not found</p>
        <router-link to="/guides" class="text-[#39FF14] font-bold underline">← guides index</router-link>
      </template>
    </div>
  </section>
</template>

<script lang="ts">
import { useAuthStore } from '@/stores/auth'
import { defineComponent } from 'vue'
import { getGuideById, type GuideItem } from '@/data/guides'

export default defineComponent({
  name: 'GuideDetail',
  props: {
    id: { type: String, required: true },
  },
  computed: {
    cabinetPath() {
      const auth = useAuthStore()
      if (!auth.isAuthenticated) return '/login'
      if (auth.role === 'admin' || auth.role === 'moderator') return '/staff'
      return '/dashboard'
    },
    guide(): GuideItem | undefined {
      return getGuideById(this.id)
    },
  },
})
</script>
