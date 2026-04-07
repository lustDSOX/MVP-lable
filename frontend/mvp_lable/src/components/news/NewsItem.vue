<template>
  <div class="group relative max-w-4xl mx-auto mb-16 ">
    
    <!-- ДЕКОРАТИВНЫЙ ЭЛЕМЕНТ: Правый верхний угол -->
    <div class="absolute -top-1/7 -right-70 w-2/3 z-10 pointer-events-none -rotate-12">
      <img src="@/assets/chrome/t_chrome.webp" 
           class="sigil-metal w-full h-full object-contain rotate-0" 
           alt="sigil-decoration">
    </div>

    <!-- ДЕКОРАТИВНЫЙ ЭЛЕМЕНТ: Левый нижний угол -->
    <div class="absolute -bottom-1/12 -left-1/5 w-1/2 z-10 pointer-events-none">
      <img src="@/assets/chrome/b_chrome.webp" 
           class="sigil-metal w-full h-full object-contain" 
           alt="sigil-decoration">
    </div>

    <div class="y2k-metal p-10 lg:p-16">

      <!-- Контент поверх текстуры -->
      <div class="relative z-20">
        
        <!-- Мета-информация (Штамповка) -->
        <div class="flex items-center justify-between mb-10">
          
          <div class="flex items-center gap-4 text-sm font-mono tracking-[0.4em] uppercase text-engraved-light">
            SOURCE SOX
          </div>

          <div class="text-sm font-mono text-engraved-light uppercase tracking-[0.2em]">
            [{{ publishedAt }}]
          </div>
        </div>

        <!-- Заголовок: Вспыхивает белым (настройка в CSS .group:hover .text-engraved) -->
        <h2 class="text-4xl md:text-6xl font-cindie uppercase italic tracking-tighter leading-none mb-8 
                   text-engraved">
          {{ title }}
        </h2>

        <!-- Описание: Вспыхивает светло-серым -->
        <p class="text-engraved-light font-montserrat leading-relaxed max-w-2xl mb-12 text-2xl">
          {{ description }}
        </p>

        <!-- Ссылка: Оставили голубой неон только для самой интерактивной кнопки -->
        <div class="flex justify-start">
          <a :href="sourceLink" target="_blank"
             class="group/link flex items-center gap-6 text-xl uppercase
                    text-engraved tracking-widest transition-all duration-300">
            <!-- Линия фрезеровки -->
            <span class="w-12 h-0.5 bg-black/80 shadow-[0_1px_0_rgba(255,255,255,0.4)] 
                         group-hover/link:w-24 group-hover:bg-white transition-all duration-500"></span>
            Access Terminal
          </a>
        </div>
      </div>

      <!-- Декор: Серийный номер -->
      <div class="absolute right-6 bottom-6 font-mono text-[10px] tracking-widest text-engraved-light opacity-60">
        LOG_ID: 00{{ Math.floor(Math.random() * 999) }} / SECTOR_01
      </div>

    </div>
  </div>
</template>

<style scoped>

  .metal-card {
      background: linear-gradient(135deg, #0f0f0f 0%, #1a1a1a 100%);
      border: 1px solid #2a2a2a;
      box-shadow: inset 0 0 20px rgba(0,0,0,0.5);
  }

</style>

<script lang="ts">
import { defineComponent } from 'vue'
import type { PropType } from 'vue'

export default defineComponent({
  name: 'NewsItem',
  props: {
    id: {
      type: Number as PropType<number>,
      required: true,
    },
    title: {
      type: String as PropType<string>,
      required: true,
    },
    description: {
      type: String as PropType<string>,
      required: true,
    },
    publishedAt: {
      type: String as PropType<string>,
      required: true,
    },
    sourceLink: {
      type: String as PropType<string | undefined>,
    },
  },
  methods: {
    formatDate(dateStr: string) {
      const date = new Date(dateStr)
      const day = String(date.getDate()).padStart(2, '0')
      const month = String(date.getMonth() + 1).padStart(2, '0')
      const year = date.getFullYear()
      return `${day}.${month}.${year}`
    },
  },
})
</script>