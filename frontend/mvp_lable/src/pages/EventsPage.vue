<template>
  <section class="min-h-screen py-20 px-4 lg:px-10 font-['Impact','Arial_Black',sans-serif] text-white overflow-hidden relative selection:bg-[#ff0000]">

    <div class="max-w-7xl mx-auto relative z-10">
      
      <!-- HEADER -->
      <div class="mb-20 flex flex-col md:flex-row items-end justify-between border-b-5 border-[#333] p-6 border-double">
        <h1 class="text-7xl lg:text-[140px] leading-none scale-y-125 uppercase tracking-tight text-white drop-shadow-[5px_5px_0_#39FF14]">
          EV<span class="text-[#ff0000]">E</span>NTS_
        </h1>
        <div class="bg-[#ff0000] text-black px-4 py-2 font-mono text-xs font-bold animate-pulse mt-4 md:mt-0 shadow-[4px_4px_0_#fff] bottom-0">
          STATUS: SELLING_OUT_FAST
        </div>
      </div>

      <!-- СПИСОК МЕРОПРИЯТИЙ -->
      <div class="grid grid-cols-1 gap-12">
        <div
          v-for="event in events"
          :key="event.id"
          class="group relative bg-[#0a0a0a] border-4 border-[#222] transition-none hover:border-[#39FF14] flex flex-col lg:flex-row shadow-[15px_15px_0_#111] hover:shadow-[15px_15px_0_#39FF14] overflow-hidden"
        >
          <!-- 1. ЛЕВАЯ ЧАСТЬ: Дата (Отрывной край билета) -->
          <div class="lg:w-48 bg-[#111] border-b-4 lg:border-b-0 lg:border-r-4 border-dashed border-[#333] p-6 flex flex-col items-center justify-center relative group-hover:bg-[#ff0000] transition-none">
            <!-- Перфорация (дырки как на билете) -->
            <div class="absolute -top-4 -right-4 w-8 h-8 bg-[#050505] rounded-full border-4 border-[#222] hidden lg:block"></div>
            <div class="absolute -bottom-4 -right-4 w-8 h-8 bg-[#050505] rounded-full border-4 border-[#222] hidden lg:block"></div>

            <div class="text-center group-hover:text-black transition-none">
              <span class="block text-4xl  leading-none uppercase italic">{{ event.date.split(' ')[0] }}</span>
              <span class="block text-xl font-bold border-t-2 border-current mt-2 pt-2">{{ event.date.split(' ')[1] }}</span>
              <span class="block text-sm font-mono mt-4 opacity-50 group-hover:text-lg group-hover:font-black">{{ event.time }}</span>
            </div>
          </div>

          <!-- 2. ЦЕНТРАЛЬНАЯ ЧАСТЬ: Инфо -->
          <div class="flex-1 p-8 relative overflow-hidden">
            <!-- Глитч-подложка -->
            <div class="absolute inset-0 bg-[url('https://www.transparenttextures.com/patterns/dust.png')] opacity-10 pointer-events-none"></div>
            
            <div class="relative z-10">
              <h3 class="text-4xl lg:text-5xl  uppercase text-white group-hover:text-[#39FF14] leading-none mb-4 tracking-tighter italic transition-none">
                {{ event.title }}
              </h3>
              
              <div class="flex gap-4 mb-6">
                <span class="bg-[#333] text-sm px-2 py-0.5 font-mono text-gray-400 group-hover:bg-white group-hover:text-black transition-none uppercase">ID: 0{{ event.id }}_ENTRY</span>
                <span class="bg-[#333] text-sm px-2 py-0.5 font-mono text-gray-400 group-hover:bg-white group-hover:text-black transition-none uppercase italic">Location: [REDACTED]</span>
              </div>

              <p class="text-gray-400 font-mono text-lg leading-tight uppercase group-hover:text-white transition-none mb-4 max-w-2xl">
                {{ event.description }}
              </p>
            </div>
          </div>

          <!-- 3. ПРАВАЯ ЧАСТЬ: CTA (Штрих-код и Кнопка) -->
          <div class="lg:w-72 bg-[#050505] p-8 flex flex-col justify-between border-t-4 lg:border-t-0 lg:border-l-4 border-[#222] group-hover:bg-black transition-none">
            
            <!-- Декор: Штрих-код -->
            <div class="opacity-20 group-hover:opacity-100 transition-opacity mb-8 flex justify-center">
               <img src="https://pngimg.com/uploads/barcode/barcode_PNG13.png" class="h-16 invert contrast-200" alt="code">
            </div>

            <a
              :href="event.link"
              target="_blank"
              class="block w-full bg-[#39FF14] text-black  uppercase text-xl py-4 text-center border-4 border-black shadow-[6px_6px_0_#fff] hover:shadow-none hover:translate-x-1.5 hover:translate-y-1.5 transition-none relative group/btn"
            >
              GET_TICKET
              <span class="absolute top-1 right-1 text-[10px] animate-ping text-red-600">●</span>
            </a>
          </div>
        </div>
      </div>

      <!-- ВИЗУАЛЬНЫЙ МУСОР (Декор внизу) -->
      <div class="mt-24 border-t-4 border-[#222] pt-8 flex flex-wrap gap-12 opacity-30">
        <div v-for="i in 3" :key="i" class="flex items-center gap-4">
           <div class="w-12 h-12 rounded-full border-4 border-[#333] flex items-center justify-center">
              <span class="text-xl">✖</span>
           </div>
           <div class="text-[10px] font-mono leading-none">
              URBAN_CULTURE_CONTROL<br>VERIFIED_BY_.SOX
           </div>
        </div>
      </div>
    </div>

    <!-- Вертикальный глитч-разделитель -->
    <div class="absolute left-0 top-0 h-full w-1 bg-[#ff0000] blur-2xl opacity-100 drop-shadow-[0px_0px_20px_#ff0000] animate-ping"></div>
    <div class="absolute right-0 top-0 h-full w-1 bg-[#ff0000] blur-2xl opacity-100 drop-shadow-[0px_0px_20px_#ff0000] animate-ping"></div>



  </section>
</template>

<style scoped>
/* Агрессивное мерцание для "SELLING OUT" */
@keyframes flicker-red {
  0%, 100% { background-color: #ff0000; color: #000; }
  50% { background-color: #000; color: #ff0000; }
}
.animate-pulse {
  animation: flicker-red 0.5s infinite steps(1);
}

/* Эффект "старого телевизора" для всей секции */
section::after {
  content: "";
  position: absolute;
  inset: 0;
  background: linear-gradient(rgba(18, 16, 16, 0) 50%, rgba(0, 0, 0, 0.2) 50%), 
              linear-gradient(90deg, rgba(255, 0, 0, 0.05), rgba(0, 255, 0, 0.02), rgba(0, 0, 255, 0.05));
  background-size: 100% 4px, 3px 100%;
  pointer-events: none;
  z-index: 50;
}
</style>

<script lang="ts">
import { defineComponent } from 'vue'

export default defineComponent({
  name: 'EventsPage',
  data() {
    return {
      events: [
        {
          id: 1,
          title: 'StreetFlow Battle Night',
          date: '12.04.2026',
          time: '20:00 – 01:00',
          description:
            'Открытый бит‑баттл в локальном стрит‑клубе. Живая сцена, диджей‑сет и фреш‑треки лицом к аудитории.',
          link: 'https://example.com/streetflow-battle',
        },
        {
          id: 2,
          title: 'Neon Freestyle Session',
          date: '18.04.2026',
          time: '19:00 – 23:00',
          description:
            'Серия фри‑стайловых сейшенов под неоновым светом. Артисты выбираются голосованием лейбла.',
          link: 'https://example.com/neon-session',
        },
        {
          id: 3,
          title: 'Underground Mixtape Release',
          date: '25.04.2026',
          time: '18:00',
          description:
            'Презентация первого микстейпа коллектива локальных фри‑стайлеров. Вход — цифровой билет‑класс.',
          link: 'https://example.com/underground-mixtape',
        },
      ] satisfies EventData[],
    }
  },
})

interface EventData {
  id: number
  title: string
  date: string
  time: string
  description: string
  link: string
}
</script>