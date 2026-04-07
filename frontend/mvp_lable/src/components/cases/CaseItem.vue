<template>
  <div class="relative group">
    
    <div class="absolute inset-0 border-4 border-black translate-x-0 translate-y-0 pointer-events-none">
        <div class="absolute inset-0 bg-[url('https://www.transparenttextures.com/patterns/carbon-fibre.png')] opacity-100"></div>
    </div>

    <div
      @click="$emit('open')"
      class="relative h-full z-10 block bg-black border-4 border-[#222] p-0 
              transition-all duration-200
              group-hover:translate-x-0 group-hover:-translate-y-4 group-hover:border-[#39FF14]  group-hover:scale-103
              group-hover:z-20 overflow-hidden"
    >

      <!-- 1. ФОНОВАЯ ТЕКСТУРА: Грязь и шум (видна всегда, усиливается при ховере) -->
      <div class="absolute inset-0 opacity-30 group-hover:opacity-[0.15] bg-[url('https://www.transparenttextures.com/patterns/stardust.png')] pointer-events-none transition-opacity"></div>
      
      <!-- Слой сканлайнов (CRT) -->
      <div class="absolute inset-0 bg-[linear-gradient(rgba(18,16,16,0)_50%,rgba(0,0,0,0.25)_50%)] bg-size-[100%_4px] pointer-events-none z-20"></div>

      <div class="flex flex-col justify-between relative z-10 h-full">
        
        <!-- ВЕРХНЯЯ ПАНЕЛЬ: Техническая разметка -->
        <div class="flex border-b-4 border-[#222] group-hover:border-[#39FF14] transition-colors">
          <!-- Логотип: как фото на пропуск -->
          <div class="w-24 h-24 bg-[#111] border-r-4 border-[#222] group-hover:border-[#39FF14] flex items-center justify-center p-3">
            <img :src="logo" alt="Logo" class="w-full h-full object-contain grayscale invert contrast-200 group-hover:invert-0 group-hover:grayscale-0 transition-all" />
          </div>
          
          <!-- Инфо-блок -->
          <div class="flex-1 p-3 flex flex-col justify-between bg-[#050505] group-hover:bg-[#39FF14] transition-colors">
            <div class="flex justify-between items-start">
              <span class="text-base text-[#444] group-hover:text-black uppercase tracking-tighter">System_Log: 00{{id}}</span>
            </div>
            <div class="text-xs font-mono text-[#39FF14] group-hover:text-black leading-none break-all opacity-50 group-hover:opacity-100">
              01010111_DATA_STREAM_X88
            </div>
          </div>
        </div>

        <!-- ЦЕНТРАЛЬНАЯ ЧАСТЬ -->
        <div class="p-6">
          <h3 class="text-4xl  text-white uppercase italic tracking-tighter leading-[0.8] mb-4 group-hover:text-[#39FF14] group-hover:translate-x-3 transition-all duration-200">
            {{ title }}
          </h3>
          
          <!-- Вместо "сигнала" — жесткий прогресс-бар в стиле Winamp -->
          <div class="h-6 w-full border-2 group-hover:border-[#39FF14] relative mb-4 flex overflow-hidden">
            <div v-for="n in 15" :key="n" 
                class="h-full w-full border-r group-hover:border-black group-hover:bg-[#39FF14] p-1  opacity-100 group-hover:opacity-100"
                :style="{ transitionDelay: n * 30 + 'ms' }">
            </div>
          </div>

          <p class="text-xl tracking-wider text-gray-500 group-hover:text-white leading-tight uppercase">
            {{ description }}
          </p>
        </div>

        <!-- НИЖНЯЯ ПАНЕЛЬ -->
        <div class="mt-2 p-4 bg-[#111] border-t-4 border-[#222] group-hover:bg-[#39FF14] group-hover:border-[#39FF14] flex items-center justify-between transition-all">
          <div class="flex items-center gap-2">
            <div class="w-2 h-2 bg-[#ff0000]  rounded-full"></div>
            <span class="text-sm tracking-wide text-white group-hover:text-black uppercase">Source_Detected</span>
          </div>
          <span class="text-xl  text-white group-hover:text-black tracking-widest">>>></span>
        </div>
      </div>
    </div>

  </div>
</template>

<style scoped>
@keyframes blink {
  50% { opacity: 0; }
}

/* Эффект дрожания при наведении */
.group:hover h3 {
  text-shadow: 2px 2px 0px #ff0000;
}
</style>

<script lang="ts">
import { defineComponent } from 'vue'
import type { PropType } from 'vue'

export default defineComponent({
  name: 'CaseItem',

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
    logo: {
      type: String as PropType<string>,
      required: true,
    },
  },

  emits: ['open']

})
</script>