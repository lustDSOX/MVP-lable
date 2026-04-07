<template>
  <!-- BACKDROP (Фон модалки с VHS-эффектами) -->
  <div 
    @click.self="$emit('close')"
    class="fixed inset-0 z-50 flex items-center justify-center p-4 font-['VT323',monospace] text-white overflow-hidden selection:bg-[#39FF14] selection:text-black"
  >
    <!-- Затемнение и шум фона -->
    <div class="absolute inset-0 bg-black/70 backdrop-blur-sm z-0"></div>
    <div class="absolute inset-0 bg-[url('https://www.transparenttextures.com/patterns/stardust.png')] opacity-30 mix-blend-color-dodge pointer-events-none z-0"></div>
    
    <!-- САМО ОКНО (Интерфейс старого терминала) -->
    <div 
      class="relative z-10 w-full max-w-5xl bg-black/90 border-2 border-[#39FF14]/50 flex flex-col max-h-[90vh] 
             shadow-[0_0_25px_5px_rgba(57,255,20,0.2)] animate-window-flicker"
    >
      <!-- Сканлайны поверх всего окна -->
      <div class="absolute inset-0 bg-[linear-gradient(rgba(18,16,16,0)_50%,rgba(0,0,0,0.4)_50%)] bg-size-[100%_4px] pointer-events-none z-20"></div>

      <!-- TOP BAR (Шапка окна) -->
      <div class="bg-[#39FF14]/50 p-2 text-black flex justify-between items-center shrink-0 border-b-2 border-black/50">
        <span class="text-xl px-2 tracking-wider">
          SYSTEM_LOG: DOSSIER_00{{ caseData.id }}
        </span>
        <button 
          @click="$emit('close')"
          class="w-8 h-8 flex items-center justify-center bg-black/20 text-[#39FF14]/50 text-2xl hover:bg-black hover:text-[#ff0000] transition-colors"
        >
          X
        </button>
      </div>

      <!-- СОДЕРЖИМОЕ ОКНА -->
      <div class="grid grid-cols-1 lg:grid-cols-12 overflow-y-auto">
        
        <!-- ЛЕВАЯ КОЛОНКА (Логотип) -->
        <div class="lg:col-span-4 border-b-2 lg:border-b-0 lg:border-r-2 border-[#39FF14]/30 p-6 flex flex-col items-center justify-center bg-black/50">
          <div class="w-full aspect-square bg-black shadow-[inset_0_0_20px_rgba(0,0,0,0.8)] border border-[#222] flex items-center justify-center p-6">
             <img :src="caseData.logo" alt="Case Logo" class="w-full h-full object-contain filter-vhs" />
          </div>
        </div>

        <!-- ПРАВАЯ КОЛОНКА (Информация) -->
        <div class="lg:col-span-8 p-6 md:p-8 flex flex-col">
          
          <!-- Заголовок кейса (с VHS-искажениями) -->
          <h2 class="text-6xl text-[#39FF14]/50 mb-6 vhs-text" :data-text="caseData.title">
            {{ caseData.title }}
          </h2>
          
          <!-- Описание -->
          <div class="mb-8">
            <p class="text-xl text-white/80 leading-snug tracking-wide vhs-text" :data-text="caseData.description">
              {{ caseData.description }}
            </p>
          </div>

          <!-- РЕЗУЛЬТАТЫ (Прогресс-бар и список) -->
          <div class="mt-auto pt-6 border-t border-[#39FF14]/30">
            <!-- Прогресс-бар -->
            <div class="h-6 w-full border border-[#39FF14]/50 flex mb-4">
              <div v-for="n in 15" :key="n" class="h-full w-full border-r border-black/50 bg-[#39FF14]/80"></div>
            </div>

            <!-- Список результатов -->
            <ul class="grid grid-cols-2 gap-x-6 gap-y-2">
              <li v-for="res in [
                  'TICKETS: 10K+', 
                  'GROWTH: 300%', 
                  'SESSIONS: 12', 
                  'ACCESS: GRANTED'
                ]" :key="res" class="flex items-center gap-2 text-lg">
                <div class="w-2 h-2 bg-[#ff0000]"></div>
                <span class="vhs-text" :data-text="res">{{ res }}</span>
              </li>
            </ul>
          </div>

        </div>
      </div>
    </div>
  </div>
</template>

<script lang="ts">
import { defineComponent, type PropType } from 'vue'

export default defineComponent({
  name: 'CaseModal',
  props: {
    caseData: {
      type: Object as PropType<{ id: number; title: string; description: string; logo: string }>,
      required: true
    }
  },
  emits: ['close'],
  mounted() {
    document.body.style.overflow = 'hidden'
  },
  unmounted() {
    document.body.style.overflow = 'auto'
  }
})
</script>

<style scoped>
/* 
  РЕКОМЕНДАЦИЯ: Для лучшего эффекта подключите шрифт 'VT323' из Google Fonts.
  @import url('https://fonts.googleapis.com/css2?family=VT323&display=swap');
*/
.bg-size-\[100\%_4px\] {
  background-size: 100% 4px;
}

/* Эффект VHS-искажений для текста */
.vhs-text {
  position: relative;
  color: white; /* Базовый цвет текста (виден слабо) */
  text-shadow: 0 0 2px rgba(57, 255, 20, 0.7); /* Зеленое свечение */
}

/* Зеленый слой (основной) */
.vhs-text::before {
  content: attr(data-text);
  position: absolute;
  left: 0;
  top: 0;
  color: #39FF14;
  z-index: 1;
  animation: text-glitch 0.05s infinite;
}

/* Красный слой (хроматическая аберрация) */
.vhs-text::after {
  content: attr(data-text);
  position: absolute;
  left: -2px;
  top: 0;
  color: #ff0000;
  mix-blend-mode: screen;
  opacity: 0.7;
  z-index: 0;
  animation: text-glitch 0.07s infinite;
}

/* Фильтры для картинки, чтобы она выглядела как на CRT-экране */
.filter-vhs {
  filter: grayscale(40%) contrast(1.2) brightness(0.9) drop-shadow(0 0 5px rgba(57, 255, 20, 0.3));
}

/* Анимация дрожания текста */
@keyframes text-glitch {
  0% { transform: translate(0, 0); }
  25% { transform: translate(1px, -1px); }
  50% { transform: translate(-1px, 1px); }
  75% { transform: translate(1px, 1px); }
  100% { transform: translate(-1px, -1px); }
}

/* Анимация мерцания всего окна */
@keyframes window-flicker {
  0%, 100% { opacity: 1; }
  50% { opacity: 0.98; }
}
.animate-window-flicker {
  animation: window-flicker 0.2s infinite;
}
</style>