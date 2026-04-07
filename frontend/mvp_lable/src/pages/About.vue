<template>
  <section class=" selection:bg-[#39FF14] selection:text-black min-h-screen py-20 px-4 lg:px-10 font-['Impact','Arial_Black',sans-serif] text-white overflow-hidden relative">

    <div class="max-w-7xl mx-auto relative z-10">
      
      <!-- HEADER SECTION -->
      <div class="pl-6 mb-20 relative">
        <div class="absolute left-75 text-[10px] font-mono text-[#39FF14] animate-pulse">
          SYSTEM_ACCESS: GRANTED // SECURITY_LEVEL: RED
        </div>

        <h1 class="variant-red">
            {{ aboutData.header.title }}
        </h1>
        
        <p class="text-xl lg:text-3xl text-[#ff0000] font-black uppercase mt-2 tracking-widest italic">
          {{ aboutData.header.subtitle }}
        </p>
        <p class="text-gray-400 font-mono text-sm max-w-xl mt-6 uppercase leading-tight">
          > {{ aboutData.header.description }}
        </p>
      </div>


      <!-- MAIN CONTENT: STORY -->
      <div class="grid lg:grid-cols-12 gap-0 border-4 border-[#222] bg-black shadow-[20px_20px_0_#111]">

        <!-- kirby -->
        <img src="@/assets/svg/pic/kirby.webp" alt="y2k_star" class="w-40 absolute right-60 top-52 blur-[0.3px]">
        
        <!-- Текстовый блок (Терминал) -->
        <div class="lg:col-span-7 p-8 border-b-4 lg:border-b-0 lg:border-r-4 border-[#222] relative overflow-hidden group">
          <div class="absolute inset-0 bg-[#ff0000] opacity-0 group-hover:opacity-10 transition-opacity"></div>
          
          <h2 class="text-5xl font-black mb-8 italic text-white flex items-center gap-4">
             <span class="w-12 h-1 bg-[#ff0000]"></span>
             {{ aboutData.story.title }}
          </h2>

          <img src="@/assets/svg/face/base.svg" alt="base_face" class="w-100 absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2">
          
          <div class="space-y-8 text-gray-300 font-mono text-lg leading-relaxed">
            <p v-for="(p, i) in aboutData.story.paragraphs" :key="i" 
              class="relative pl-10 border-l-4 border-[#222] hover:border-[#39FF14] transition-colors group/item">
              <span class="absolute left-1 -top-2 text-[#39FF14] font-blac group-hover/item:text-white">
                >>
              </span>
              {{ p }}
            </p>
          </div>
        </div>

        <!-- Визуальный блок (Image Slot) -->
        <div class="lg:col-span-5 bg-[#0a0a0a] relative p-8 flex items-center justify-center min-h-100 bg-[url('https://www.transparenttextures.com/patterns/dust.png')]">
          <div class="w-full aspect-4/3 relative border-4 border-white shadow-[10px_10px_0_#39FF14] overflow-hidden group z-20">
            <img src="@/assets/alert.jpg" 
                 class="w-full h-full object-cover grayscale contrast-125" 
                 alt="history_image">
            <div class="absolute top-4 right-4 bg-red-600 text-white px-2 py-1 text-[10px] animate-pulse italic">LIVE_FEED</div>
          </div>
        </div>
      </div>

      <!-- PHILOSOPHY: Memory Card Grid -->
      <div class="mt-24">
        <h2 class="text-6xl font-black italic mb-12 text-center text-transparent stroke-text uppercase">
          {{ aboutData.philosophy.title }}
        </h2>
        
        <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
           <PhilosophyCard 
              v-for="item in aboutData.philosophy.items" 
              :key="item.id" 
              :item="item" 
            />  
        </div>

      </div>

      <!-- SLOGAN -->
      <div class="mt-32 relative text-center border-y-4 border-[#222] py-12 bg-[url('https://www.transparenttextures.com/patterns/carbon-fibre.png')] overflow-hidden">
        <div class="absolute inset-0 bg-[#39FF14] opacity-5 mix-blend-color"></div>
        <p class="text-3xl lg:text-6xl font-black uppercase italic tracking-wide text-white drop-shadow-[4px_4px_0_#ff0000] px-4">
          {{ aboutData.slogan }}
        </p>
        <div class="mt-8 flex justify-center gap-4">
           <div v-for="i in 5" :key="i" class="w-8 h-2 bg-[#ff0000]"></div>
        </div>
      </div>

    </div>

    <!-- CD-диск анимированный -->
    <img src="@/assets/svg/pic/disc.svg" alt="y2k_disc" class="absolute -right-100 top-2/5 w-200 opacity-80 pointer-events-none animate-spin-slow z-0"> </img>

    <!-- Котозавр слева -->
    <img src="@/assets/svg/pic/stay_cat.svg" alt="y2k_cat" class="absolute -bottom-20 -left-60">

    <!-- Star -->
    <img src="@/assets/svg/pic/metal_star.webp" alt="metal_star" class="absolute top-70 left-25 w-1/5">

    <!-- Декор: летающий глитч-элемент -->
    <div class="absolute top-2/12 -right-30 w-120 h-2 bg-[#ff0000] opacity-20 blur-sm animate-pulse rotate-45"></div>

  </section>
</template>

<style scoped>
.stroke-text {
  color: transparent;
  -webkit-text-stroke: 1px rgba(255,255,255,0.4);
}

.stroke-text::selection {
  color: black;
  -webkit-text-stroke: 0;
}

.animate-spin-slow {
  animation: spin 12s linear infinite;
}

@keyframes spin {
  from { transform: rotate(0deg); }
  to { transform: rotate(360deg); }
}

/* Кастомный индустриальный скролл */
::-webkit-scrollbar {
  width: 10px;
}
::-webkit-scrollbar-track {
  background: #000;
}
::-webkit-scrollbar-thumb {
  background: #39FF14;
  border: 2px solid #000;
}
</style>


<script lang="ts">
import PhilosophyCard from "@/components/about/PhilosophyCard.vue";
import { aboutData } from "@/data/about";

export default {
  name: 'AboutPage',

  data(){
    return{
      aboutData
    }
  },

  components:{
    PhilosophyCard
  }
}
</script>