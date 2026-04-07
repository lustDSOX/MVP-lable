<template>
  <!-- ОСНОВНОЙ КОНТЕЙНЕР: Плотный Dark Y2K Брутализм -->
  <section class="min-h-screen pt-32 pb-20 px-4 lg:px-10 font-['Inter',sans-serif] text-white overflow-hidden relative selection:bg-[#ff0000] selection:text-white bg-black">

    <!-- ГЛОБАЛЬНЫЙ ФОН: Y2K сетка + Статический CRT шум -->
    <div class="absolute inset-0 pointer-events-none z-0 crt-noise opacity-[0.15] mix-blend-screen"></div>
    
    <!-- ИЗОБРАЖЕНИЕ 1: Глаз (Тяжелый силуэт на заднем плане) -->
    <div class="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-[120vw] md:w-[70vw] opacity-[0.04] pointer-events-none z-0">
      <img src="@/assets/svg/y2k/eye.svg" alt="Portal" class="w-full h-full object-contain invert">
    </div>

    <div class="max-w-7xl mx-auto relative z-10">
      
      <!-- HEADER -->
      <!-- Жесткая подчеркивающая линия и системный текст -->
      <div class="mb-16 flex flex-col items-start border-b-4 border-[#222] pb-6 relative">
        <div class="absolute top-0 right-0 bg-[#ff0000] text-white font-['JetBrains_Mono',monospace] text-xs font-bold px-3 py-1 uppercase tracking-widest rotate-2">
          System_Breach
        </div>
        
        <!-- Ваш глобальный H1 (variant-red) -->
        <h1 class="variant-corrupted-brutal m-0" data-text="ARTIST_GUIDES">
          ARTIST_GUIDES
        </h1>
      </div>

      <!-- ГРИД КАРТОЧЕК: Жесткая табличная структура -->
      <!-- Толстые рамки, никаких скруглений -->
      <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 border-t-2 border-l-2 border-[#333] bg-black">
        <router-link
          v-for="(guide, index) in guides"
          :key="guide.id"
          :to="{ name: 'GuideDetail', params: { id: guide.id.toString() } }"
          class="group relative p-8 transition-none overflow-hidden cursor-crosshair h-105 flex flex-col border-b-2 border-r-2 border-[#333] hover:bg-[#050505]"
        >
          <!-- ИЗОБРАЖЕНИЕ 2: Существо при ховере -->
          <!-- Появляется резко (transition-none), инвертируется в белый силуэт -->
          <img 
            src="@/assets/svg/y2k/creature-gun.svg" 
            class="absolute -bottom-8 -right-8 w-64 opacity-0 group-hover:opacity-100 transition-none z-0 invert filter grayscale group-hover:animate-harsh-glitch pointer-events-none"
            alt="Anomaly"
          >

          <!-- КОНТЕНТ КАРТОЧКИ -->
          <div class="relative z-10 h-full flex flex-col justify-between">
            <!-- Верх: Номер и тег -->
            <div class="flex justify-between items-start mb-auto">
              <span class="text-6xl font-['Archivo_Black',sans-serif] text-white leading-none tracking-tighter group-hover:text-[#ff0000]">
                0{{index + 1}}
              </span>
              <div class="border border-[#444] px-2 py-1 font-['JetBrains_Mono',monospace] font-bold text-[10px] uppercase tracking-widest text-[#666] group-hover:border-[#ff0000] group-hover:text-[#ff0000]">
                .DATA
              </div>
            </div>

            <!-- Низ: Заголовок и Описание -->
            <div class="mt-auto">
              <h3 class="text-3xl font-['Archivo_Black',sans-serif] text-white px-1 uppercase leading-[1.3] tracking-tight mb-4 wrap-break-word">
                <span class="group-hover:bg-[#ff0000] group-hover:text-black box-decoration-clone">
                  {{ guide.title }}
                </span>
              </h3>
              
              <!-- ЧИТАЕМОСТЬ: При ховере текст получает черный фон, перекрывая картинку -->
              <p class="font-['Inter',sans-serif] text-xs uppercase leading-relaxed tracking-widest text-gray-400 text-justify px-1">
                <span class="group-hover:bg-black group-hover:text-white box-decoration-clone leading-[1.8] py-0.5">
                  {{ guide.description }}
                </span>
              </p>
            </div>
          </div>
        </router-link>
      </div>

      <!-- ВИЗУАЛЬНЫЙ МЕРЧ: Инструкция внизу -->
      <div class="mt-24 p-8 border-2 border-dashed border-[#333] bg-black relative overflow-hidden group">
        <!-- ИЗОБРАЖЕНИЕ 2 (Существо): Стоит сбоку в блоке -->
        <img src="@/assets/svg/y2k/man.svg" class="absolute -left-10 -bottom-10 h-[150%] opacity-10 grayscale invert rotate-[-15deg] pointer-events-none">
        
        <div class="absolute -top-3 left-10 bg-black text-[#ff0000] border border-[#ff0000] px-4 py-1 text-xl italic z-10">FATAL_ERROR</div>
        
        <div class="flex flex-col md:flex-row gap-8 items-center relative z-10 pl-10 md:pl-32">
          <div class="flex-1 text-gray-400 font-mono text-xs md:text-sm uppercase leading-relaxed text-justify">
            Все гайды предоставлены исключительно для ознакомления. Использование полученных знаний может привести к <span class="text-white bg-black px-1 line-through">перегрузке серверов</span> потере контроля над разумом и взлому музыкальных чартов. 
            <span class="text-[#ff0000] font-bold block mt-2">.SOX IS NOT RESPONSIBLE FOR THE ENTITIES YOU SUMMON.</span>
          </div>
          <div class="shrink-0 flex flex-col items-center">
            <img src="https://pngimg.com/uploads/barcode/barcode_PNG13.png" class="h-16 invert opacity-50 mb-2" alt="barcode">
            <span class="font-mono text-[8px] tracking-widest text-[#666]">SCAN_AT_YOUR_OWN_RISK</span>
          </div>
        </div>
      </div>


    </div>
  </section>
</template>

<style scoped>
/* Y2K Точечная сетка */
.y2k-bg-grid {
  background-size: 20px 20px;
  background-image: radial-gradient(circle, #222 1px, transparent 1px);
}

/* Статический CRT шум для фактуры "старого монитора" */
.crt-noise {
  background-image: url('data:image/svg+xml;utf8,%3Csvg viewBox="0 0 200 200" xmlns="http://www.w3.org/2000/svg"%3E%3Cfilter id="noiseFilter"%3E%3CfeTurbulence type="fractalNoise" baseFrequency="0.9" numOctaves="3" stitchTiles="stitch"/%3E%3C/filter%3E%3Crect width="100%25" height="100%25" filter="url(%23noiseFilter)"/%3E%3C/svg%3E');
}

/* Жесткий глитч (без неона, просто смещение координат) */
@keyframes harsh-glitch {
  0%, 100% { transform: translate(0, 0); }
  25% { transform: translate(-3px, 2px); }
  50% { transform: translate(3px, -1px); }
  75% { transform: translate(-1px, -3px); }
}
.animate-harsh-glitch {
  animation: harsh-glitch 0.2s steps(2) infinite;
}

/* box-decoration-clone позволяет фону обтекать каждую строку текста ровно */
.box-decoration-clone {
  -webkit-box-decoration-break: clone;
  box-decoration-break: clone;
}
</style>

<script lang="ts">
import { defineComponent } from 'vue'

export default defineComponent({
  name: 'GuidesPage',
  data() {
    return {
      guides: [
        {
          id: 1,
          title: 'Как начать записывать свои треки дома',
          description: 'Простое пошаговое руководство по записи первых треков без студии. От микширования до базовой сессии в DAW.',
        },
        {
          id: 2,
          title: 'Как писать текст, чтобы его слышали',
          description: 'Секреты написания текстов, которые цепляют слушателя. Ритмика, образы, эмоции.',
        },
        {
          id: 3,
          title: 'Личный кабинет артиста: как работать с отчётами',
          description: 'Как смотреть статистику, билеты и отчёты, чтобы понимать, куда движется твой трек.',
        },
      ] satisfies GuideItemData[],
    }
  },
})

interface GuideItemData {
  id: number
  title: string
  description: string
}
</script>