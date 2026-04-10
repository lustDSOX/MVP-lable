<template>


  <section class="min-h-screen  pt-32 pb-20 px-4 lg:px-10 font-['Impact','Arial_Black',sans-serif] text-white overflow-hidden relative selection:bg-[#ff0000] selection:text-white">

    <div class="max-w-6xl mx-auto relative z-10">
      
      <!-- HEADER: Световое табло -->
      <div class="flex flex-col md:flex-row justify-between items-end pb-6 relative">
        <div class="relative">
          <h1 class="font-planet h1-metal-textured" data-text="NEWS_LOG">
            NEWS_LOG
          </h1>
        </div>
        
        <!-- Технический блок справа -->
        <div class="hidden lg:block text-right font-mono text-[12px] text-gray-500 uppercase">
          <p>Frequency: 142.06 MHz</p>
          <p>Location: [ REDACTED ]</p>
          <p>Signal: 100% SECURE</p>
        </div>
      </div>

      <div class="relative w-screen left-1/2 -translate-x-1/2 h-10 mb-20 flex items-center justify-center overflow-hidden">
        <div class="absolute inset-0 bg-chain-placeholder bg-repeat-x bg-center bg-size-[auto_300%]"></div>
      </div>

      <!-- СПИСОК НОВОСТЕЙ -->
      <div v-if="newsList.length > 0" class="space-y-12">
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

      <!-- СОСТОЯНИЯ: Loading / Empty -->
      <div v-if="loading" class="flex flex-col items-center justify-center py-20 border-4 border-dashed border-[#222]">
        <div class="w-16 h-16 border-8 border-t-[#39FF14] border-[#111] rounded-full animate-spin mb-4"></div>
        <p class="text-2xl font-black text-[#39FF14] animate-pulse italic uppercase">CONNECTING_TO_SATELLITE...</p>
      </div>

      <div v-if="newsList.length === 0 && !loading" class="bg-[#111] border-4 border-[#ff0000] p-12 text-center shadow-[15px_15px_0_#000]">
        <h2 class="text-4xl font-black text-[#ff0000] uppercase italic">NO_DATA_PACKETS_FOUND</h2>
        <p class="text-gray-500 font-mono mt-4 uppercase">System is waiting for upcoming urban transmissions.</p>
      </div>

    </div>

    <img src="@/assets/chrome/chain.png" alt="chrome_chain" class="absolute h-250 rotate-35 -top-28 -left-70">

    <div class="absolute bg-chain-placeholder w-[110%] h-10 bg-repeat-x bg-center bg-size-[auto_300%] rotate-10 -right-10 top-1/4"></div>
    <div class="absolute bg-chain-placeholder w-[110%] h-10 bg-repeat-x bg-center bg-size-[auto_300%] -rotate-10 -right-10 top-1/2"></div>
    <div class="absolute bg-chain-placeholder w-[120%] h-10 bg-repeat-x bg-center bg-size-[auto_300%] rotate-30 -right-40 bottom-1/3"></div>


    <img src="@/assets/chrome/chain_circle.png" alt="chrome_chain" class="absolute h-180 top-5/11 -right-25 rotate-2 z-10">

    <img src="@/assets/chrome/chain_flow.png" alt="chrome_chain" class="absolute h-180 -left-50 bottom-10 rotate-100">

    <!-- star face -->
    <div class="absolute h-30 w-30 left-20 top-5/11 mask-star-face bg-[#1b1b1b11] -rotate-25"></div>

    <!-- fairy cat -->
    <div class="absolute h-80 w-80 right-20 -bottom-15 mask-fairy-cat bg-[linear-gradient(135deg,#333_0%,#999_38%,#fff_48%,#fff_50%,#000_52%,#333_75%,#111_100%)] drop-shadow-[0_0_10px_rgba(255,255,255,0.2)]"></div>
    
    <!-- text together -->
    <div class="absolute h-80 w-80 right-20 -bottom-15 mask-text bg-[linear-gradient(135deg,#333_0%,#999_38%,#fff_48%,#fff_50%,#000_52%,#333_75%,#111_100%)] drop-shadow-[0_0_10px_rgba(255,255,255,0.2)]"></div>


  </section>
</template>

<style scoped>

.mask-star-face {
  /* Путь к твоему SVG */
  -webkit-mask-image: url('@/assets/svg/face/star_face.svg');
  -webkit-mask-size: contain;
  -webkit-mask-repeat: no-repeat;
  -webkit-mask-position: center;
  
  /* Стандартные свойства для кроссбраузерности */
  mask-image: url('@/assets/svg/face/star_face.svg');
  mask-size: contain;
  mask-repeat: no-repeat;
  mask-position: center;
}


.mask-fairy-cat {
  /* Путь к твоему SVG */
  -webkit-mask-image: url('@/assets/svg/pic/fairy_cat.svg');
  -webkit-mask-size: contain;
  -webkit-mask-repeat: no-repeat;
  -webkit-mask-position: center;
  
  /* Стандартные свойства для кроссбраузерности */
  mask-image: url('@/assets/svg/pic/fairy_cat.svg');
  mask-size: contain;
  mask-repeat: no-repeat;
  mask-position: center;
}

.mask-text {
  /* Путь к твоему SVG */
  -webkit-mask-image: url('@/assets/svg/text/together.svg');
  -webkit-mask-size: contain;
  -webkit-mask-repeat: no-repeat;
  -webkit-mask-position: center;
  
  /* Стандартные свойства для кроссбраузерности */
  mask-image: url('@/assets/svg/text/together.svg');
  mask-size: contain;
  mask-repeat: no-repeat;
  mask-position: center;
}

.bg-chain-placeholder {
    background-image: url("@/assets/chrome/chain_bg.png");
  }

@keyframes marquee {
  0% { transform: translateX(0); }
  100% { transform: translateX(-50%); }
}
.animate-marquee {
  display: flex;
  width: max-content;
  animation: marquee 50s linear infinite;
}
</style>

<script lang="ts">
import { defineComponent } from 'vue'
import NewsItem from '@/components/news/NewsItem.vue'

export default defineComponent({
  name: 'NewsPage',
  components: {
    NewsItem,
  },
  data() {
    return {
      newsList: [] as NewsItemData[],
      loading: true,
    }
  },
  async created() {
    try {
      const data: NewsItemData[] = [
        {
          id: 1,
          title: 'CLASS TICKETS выпуск нового альбома',
          description: 'Первый релиз лейбла в рамках нового урбан‑сезона. Уже доступен в цифровых магазинах и в личном кабинете артистов.',
          publishedAt: '2026-03-20',
          sourceLink: 'https://example.com/album-release',
        },
        {
          id: 2,
          title: 'Открыта продажа билетов на StreetFlow Battle Night',
          description: 'Новый пакет классов теперь включает доступ к вечерним стрит‑баттлам без ограничений числа участий.',
          publishedAt: '2026-03-22',
          sourceLink: 'https://example.com/tickets',
        },
        {
          id: 3,
          title: 'Личный кабинет артиста стал доступен всем участникам',
          description: 'Артисты получили доступ к статистике прослушиваний, билетов и отчётов по релизам.',
          publishedAt: '2026-03-24',
          sourceLink: 'https://example.com/dashboard',
        },
      ]
      this.newsList = data
    } catch (err) {
      console.error(err)
    } finally {
      this.loading = false
    }
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