<template>
  <section class="min-h-screen pt-20 sm:pt-28 md:pt-32 pb-12 sm:pb-20 px-4 lg:px-10 font-['Impact','Arial_Black',sans-serif] text-white overflow-hidden relative selection:bg-[#ff0000] selection:text-white">

    <div class="max-w-6xl mx-auto relative z-10">
      <div class="flex flex-col md:flex-row justify-between items-end pb-2 sm:pb-4 md:pb-6 relative">
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

      <!-- Mobile: metal double-line divider (not a solid green bar) -->
      <div class="md:hidden mb-6 mt-1 px-1" aria-hidden="true">
        <div class="h-px bg-gradient-to-r from-transparent via-[#39FF14] to-transparent opacity-80"></div>
        <div class="flex items-center justify-center gap-1 my-1.5">
          <span v-for="n in 12" :key="n" class="w-1.5 h-1.5 border border-[#39FF14]/70 bg-black rotate-45"></span>
        </div>
        <div class="h-px bg-gradient-to-r from-transparent via-[#555] to-transparent"></div>
      </div>

      <!-- Desktop: chain strip -->
      <div class="hidden md:flex relative w-screen left-1/2 -translate-x-1/2 h-10 mb-20 items-center justify-center overflow-hidden">
        <div
          class="absolute inset-0"
          :class="decorReady ? 'bg-chain-placeholder bg-repeat-x bg-center bg-size-[auto_300%]' : 'bg-[#39FF14]/20'"
        ></div>
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
      <div class="decor-fade absolute bg-chain-placeholder w-[110%] h-10 bg-repeat-x bg-center bg-size-[auto_300%] rotate-10 -right-10 top-1/4"></div>
      <div class="decor-fade absolute bg-chain-placeholder w-[110%] h-10 bg-repeat-x bg-center bg-size-[auto_300%] -rotate-10 -right-10 top-1/2"></div>
      <div class="decor-fade absolute bg-chain-placeholder w-[120%] h-10 bg-repeat-x bg-center bg-size-[auto_300%] rotate-30 -right-40 bottom-1/3"></div>
      <img
        src="@/assets/chrome/chain_circle.png"
        alt=""
        decoding="async"
        fetchpriority="low"
        class="decor-fade absolute h-180 top-5/11 -right-25 rotate-2 z-10 select-none"
        @load="onDecorImg"
      >
      <img
        src="@/assets/chrome/chain_flow.png"
        alt=""
        decoding="async"
        fetchpriority="low"
        class="decor-fade absolute h-180 -left-50 bottom-10 rotate-100 select-none"
        @load="onDecorImg"
      >
      <div class="decor-fade absolute h-30 w-30 left-20 top-5/11 mask-star-face bg-[#1b1b1b11] -rotate-25"></div>
      <div class="decor-fade absolute h-80 w-80 right-20 -bottom-15 mask-fairy-cat bg-[linear-gradient(135deg,#333_0%,#999_38%,#fff_48%,#fff_50%,#000_52%,#333_75%,#111_100%)] drop-shadow-[0_0_10px_rgba(255,255,255,0.2)]"></div>
      <div class="decor-fade absolute h-80 w-80 right-20 -bottom-15 mask-text bg-[linear-gradient(135deg,#333_0%,#999_38%,#fff_48%,#fff_50%,#000_52%,#333_75%,#111_100%)] drop-shadow-[0_0_10px_rgba(255,255,255,0.2)]"></div>
    </div>
  </section>
</template>

<style scoped>
.mask-star-face {
  -webkit-mask-image: url('@/assets/svg/face/star_face.svg');
  -webkit-mask-size: contain;
  -webkit-mask-repeat: no-repeat;
  -webkit-mask-position: center;
  mask-image: url('@/assets/svg/face/star_face.svg');
  mask-size: contain;
  mask-repeat: no-repeat;
  mask-position: center;
}
.mask-fairy-cat {
  -webkit-mask-image: url('@/assets/svg/pic/fairy_cat.svg');
  -webkit-mask-size: contain;
  -webkit-mask-repeat: no-repeat;
  -webkit-mask-position: center;
  mask-image: url('@/assets/svg/pic/fairy_cat.svg');
  mask-size: contain;
  mask-repeat: no-repeat;
  mask-position: center;
}
.mask-text {
  -webkit-mask-image: url('@/assets/svg/text/together.svg');
  -webkit-mask-size: contain;
  -webkit-mask-repeat: no-repeat;
  -webkit-mask-position: center;
  mask-image: url('@/assets/svg/text/together.svg');
  mask-size: contain;
  mask-repeat: no-repeat;
  mask-position: center;
}
@media (min-width: 768px) {
  .bg-chain-placeholder {
    background-image: url("@/assets/chrome/chain_bg.png");
  }
}
.decor-fade {
  opacity: 0;
  transition: opacity 0.8s ease;
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
  created() {
    this.newsList = [
      {
        id: 1,
        title: 'CLASS TICKETS выпуск нового альбома',
        description:
          'Первый релиз лейбла в рамках нового урбан‑сезона. Уже доступен в цифровых магазинах и в личном кабинете артистов.',
        publishedAt: '2026-03-20',
        sourceLink: 'https://example.com/album-release',
      },
      {
        id: 2,
        title: 'Открыта продажа билетов на StreetFlow Battle Night',
        description:
          'Новый пакет классов теперь включает доступ к вечерним стрит‑баттлам без ограничений числа участий.',
        publishedAt: '2026-03-22',
        sourceLink: 'https://example.com/tickets',
      },
      {
        id: 3,
        title: 'Личный кабинет артиста стал доступен всем участникам',
        description:
          'Артисты получили доступ к статистике прослушиваний, билетов и отчётов по релизам.',
        publishedAt: '2026-03-24',
        sourceLink: 'https://example.com/dashboard',
      },
    ]
  },
})

interface NewsItemData {
  id: number
  title: string
  description: string
  publishedAt: string
  sourceLink?: string
}
</script>
