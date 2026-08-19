<template>
  <section class="min-h-screen pt-20 sm:pt-28 md:pt-32 pb-12 sm:pb-20 px-4 lg:px-10 font-['Impact','Arial_Black',sans-serif] text-white overflow-hidden relative selection:bg-[#ff0000] selection:text-white">

    <div class="max-w-6xl mx-auto relative z-10">
      <div class="flex flex-col md:flex-row justify-between items-end pb-4 sm:pb-4 md:pb-6 relative">
        <div class="relative">
          <h1 class="font-planet h1-metal-textured" data-text="NEWS_LOG">
            NEWS_LOG
          </h1>
        </div>
        <div class="hidden lg:block text-right font-mono text-[12px] text-gray-500 uppercase">
          <p>Frequency: 142.06 MHz</p>
          <p>Location: [ REDACTED ]</p>
          <p>Signal: 100% SECURE</p>
        </div>
      </div>

      <!-- Desktop: chain strip only -->
      <div class="hidden md:flex relative w-screen left-1/2 -translate-x-1/2 h-10 mb-20 items-center justify-center overflow-hidden">
        <div
          class="absolute inset-0"
          :class="decorReady ? 'bg-chain-placeholder bg-repeat-x bg-center bg-size-[auto_300%]' : 'bg-[#39FF14]/20'"
        ></div>
      </div>

      <div v-if="newsList.length > 0" class="space-y-5 sm:space-y-8 md:space-y-12 mt-2 md:mt-0">
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

      <div v-if="newsList.length === 0" class="bg-[#111] border-4 border-[#ff0000] p-12 text-center shadow-[15px_15px_0_#000]">
        <h2 class="text-4xl font-black text-[#ff0000] uppercase italic">NO_DATA_PACKETS_FOUND</h2>
        <p class="text-gray-500 font-mono mt-4 uppercase">System is waiting for upcoming urban transmissions.</p>
      </div>
    </div>

    <div
      v-if="showDecor"
      class="absolute inset-0 pointer-events-none overflow-hidden"
      :class="{ 'decor-ready': decorReady }"
      aria-hidden="true"
    >
      <img
        src="@/assets/chrome/chain.png"
        alt=""
        decoding="async"
        fetchpriority="low"
        class="decor-fade absolute h-250 rotate-35 -top-28 -left-70 select-none"
        @load="onDecorImg"
      >
      <div class="decor-fade absolute bg-chain-placeholder w-[110%] h-10 bg-repeat-x bg-center bg-size-[auto_300%] rotate-12 top-1/3 -left-10 opacity-40"></div>
      <div class="decor-fade absolute bg-chain-placeholder w-[110%] h-10 bg-repeat-x bg-center bg-size-[auto_300%] -rotate-6 bottom-1/4 -right-10 opacity-30"></div>
      <img
        src="@/assets/chrome/chain.png"
        alt=""
        decoding="async"
        fetchpriority="low"
        class="decor-fade absolute h-200 -rotate-20 bottom-10 -right-40 select-none opacity-50"
        @load="onDecorImg"
      >
    </div>
  </section>
</template>

<style scoped>
.decor-fade {
  opacity: 0;
  transition: opacity 0.6s ease;
}
.decor-ready .decor-fade {
  opacity: 1;
}
</style>

<script lang="ts">
import { defineComponent } from 'vue'
import NewsItem from '@/components/news/NewsItem.vue'

export default defineComponent({
  name: 'NewsPage',
  components: { NewsItem },
  data() {
    return {
      newsList: [] as NewsItemData[],
      showDecor: false,
      decorReady: false,
      _decorLoaded: 0,
      _idleHandle: 0 as number,
    }
  },
  created() {
    this.newsList = []
  },
  mounted() {
    const mq = window.matchMedia('(min-width: 768px)')
    const schedule = () => {
      if (!mq.matches) {
        this.showDecor = false
        this.decorReady = false
        return
      }
      const start = () => {
        this.showDecor = true
        window.setTimeout(() => {
          this.decorReady = true
        }, 400)
      }
      if ('requestIdleCallback' in window) {
        this._idleHandle = (window as any).requestIdleCallback(start, { timeout: 1200 })
      } else {
        this._idleHandle = window.setTimeout(start, 600) as unknown as number
      }
    }
    schedule()
    mq.addEventListener?.('change', schedule)
    ;(this as any)._mq = mq
    ;(this as any)._mqHandler = schedule

    import('@/stores/cms').then(({ useCmsStore }) => {
      const cms = useCmsStore()
      cms.hydrate()
      this.newsList = cms.publishedNews.map((n) => ({
        id: n.id as any,
        title: n.title,
        description: n.excerpt || n.body,
        publishedAt: n.date,
        sourceLink: '#',
      }))
    })
  },
  unmounted() {
    const mq = (this as any)._mq
    const handler = (this as any)._mqHandler
    if (mq && handler) mq.removeEventListener?.('change', handler)
    if (this._idleHandle) {
      if ('cancelIdleCallback' in window) (window as any).cancelIdleCallback(this._idleHandle)
      else clearTimeout(this._idleHandle)
    }
  },
  methods: {
    onDecorImg() {
      this._decorLoaded += 1
      if (this._decorLoaded >= 2) this.decorReady = true
    },
  },
})

interface NewsItemData {
  id: number | string
  title: string
  description: string
  publishedAt: string
  sourceLink?: string
}
</script>
