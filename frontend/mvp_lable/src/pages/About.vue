<template>
  <section class="selection:bg-[#39FF14] selection:text-black min-h-screen py-10 sm:py-16 lg:py-20 px-4 lg:px-10 font-['Impact','Arial_Black',sans-serif] text-white overflow-hidden relative">

    <div class="max-w-7xl mx-auto relative z-10">
      
      <div class="pl-2 sm:pl-6 mb-12 sm:mb-20 relative">
        <div class="absolute left-4 sm:left-20 md:left-40 lg:left-75 top-0 text-[8px] sm:text-[10px] font-mono text-[#39FF14] animate-pulse max-w-[70%]">
          SYSTEM_ACCESS: GRANTED // SECURITY_LEVEL: RED
        </div>

        <h1 class="variant-red text-4xl sm:text-5xl md:text-6xl lg:text-8xl">
            {{ aboutData.header.title }}
        </h1>
        
        <p class="text-lg sm:text-xl lg:text-3xl text-[#ff0000] font-black uppercase mt-2 tracking-widest italic">
          {{ aboutData.header.subtitle }}
        </p>
        <p class="text-gray-400 font-mono text-xs sm:text-sm max-w-xl mt-4 sm:mt-6 uppercase leading-tight">
          > {{ aboutData.header.description }}
        </p>
      </div>

      <div class="grid grid-cols-1 lg:grid-cols-12 gap-0 border-2 sm:border-4 border-[#222] bg-black shadow-[8px_8px_0_#111] sm:shadow-[20px_20px_0_#111]">

        <img 
          src="@/assets/svg/pic/kirby.webp" 
          alt="y2k_star" 
          class="w-20 sm:w-28 md:w-40 max-w-[25vw] absolute right-4 sm:right-20 md:right-40 lg:right-60 top-32 sm:top-40 md:top-52 blur-[0.3px] hidden md:block pointer-events-none"
        >
        
        <div class="lg:col-span-7 p-4 sm:p-6 md:p-8 border-b-2 sm:border-b-4 lg:border-b-0 lg:border-r-4 border-[#222] relative overflow-hidden group">
          <div class="absolute inset-0 bg-[#ff0000] opacity-0 group-hover:opacity-10 transition-opacity"></div>
          
          <h2 class="text-3xl sm:text-4xl md:text-5xl font-black mb-6 sm:mb-8 italic text-white flex items-center gap-2 sm:gap-4">
             <span class="w-8 sm:w-12 h-1 bg-[#ff0000] shrink-0"></span>
             {{ aboutData.story.title }}
          </h2>

          <img 
            src="@/assets/svg/face/base.svg" 
            alt="base_face" 
            class="w-48 sm:w-64 md:w-80 lg:w-100 max-w-[70%] absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 opacity-30 sm:opacity-50 pointer-events-none object-contain"
          >
          
          <div class="space-y-6 sm:space-y-8 text-gray-300 font-mono text-sm sm:text-base md:text-lg leading-relaxed relative z-10">
            <p v-for="(p, i) in aboutData.story.paragraphs" :key="i" 
              class="relative pl-8 sm:pl-10 border-l-2 sm:border-l-4 border-[#222] hover:border-[#39FF14] transition-colors group/item">
              <span class="absolute left-0.5 sm:left-1 -top-1 sm:-top-2 text-[#39FF14] font-black group-hover/item:text-white text-xs sm:text-base">
                >>
              </span>
              {{ p }}
            </p>
          </div>
        </div>

        <div class="lg:col-span-5 bg-[#0a0a0a] relative p-4 sm:p-6 md:p-8 flex items-center justify-center min-h-[220px] sm:min-h-80 md:min-h-100 bg-[url('https://www.transparenttextures.com/patterns/dust.png')]">
          <div class="w-full max-w-sm mx-auto aspect-4/3 relative border-2 sm:border-4 border-white shadow-[6px_6px_0_#39FF14] sm:shadow-[10px_10px_0_#39FF14] overflow-hidden group z-20">
            <img 
              src="@/assets/alert.jpg" 
              class="w-full h-full object-cover object-center grayscale contrast-125" 
              alt="history_image"
            >
            <div class="absolute top-2 sm:top-4 right-2 sm:right-4 bg-red-600 text-white px-1.5 sm:px-2 py-0.5 sm:py-1 text-[8px] sm:text-[10px] animate-pulse italic">LIVE_FEED</div>
          </div>
        </div>
      </div>

      <div class="mt-12 sm:mt-16 md:mt-24">
        <h2 class="text-3xl sm:text-4xl md:text-5xl lg:text-6xl font-black italic mb-8 sm:mb-12 text-center text-transparent stroke-text uppercase px-2">
          {{ aboutData.philosophy.title }}
        </h2>
        
        <div class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4 sm:gap-6">
           <PhilosophyCard 
              v-for="item in aboutData.philosophy.items" 
              :key="item.id" 
              :item="item" 
            />  
        </div>
      </div>

      <div class="mt-16 sm:mt-24 md:mt-32 relative text-center border-y-2 sm:border-y-4 border-[#222] py-8 sm:py-12 bg-[url('https://www.transparenttextures.com/patterns/carbon-fibre.png')] overflow-hidden">
        <div class="absolute inset-0 bg-[#39FF14] opacity-5 mix-blend-color"></div>
        <p class="text-xl sm:text-3xl lg:text-6xl font-black uppercase italic tracking-wide text-white drop-shadow-[2px_2px_0_#ff0000] sm:drop-shadow-[4px_4px_0_#ff0000] px-4">
          {{ aboutData.slogan }}
        </p>
        <div class="mt-6 sm:mt-8 flex justify-center gap-2 sm:gap-4">
           <div v-for="i in 5" :key="i" class="w-4 sm:w-8 h-1.5 sm:h-2 bg-[#ff0000]"></div>
        </div>
      </div>

    </div>

    <img 
      src="@/assets/svg/pic/disc.svg" 
      alt="y2k_disc" 
      class="absolute -right-32 sm:-right-48 md:-right-64 lg:-right-100 top-1/3 sm:top-2/5 w-48 sm:w-72 md:w-96 lg:w-200 max-w-[50vw] opacity-40 sm:opacity-80 pointer-events-none animate-spin-slow z-0 hidden sm:block"
    >

    <img 
      src="@/assets/svg/pic/stay_cat.svg" 
      alt="y2k_cat" 
      class="absolute -bottom-10 sm:-bottom-16 md:-bottom-20 -left-24 sm:-left-40 md:-left-60 w-40 sm:w-56 md:w-72 max-w-[45vw] pointer-events-none opacity-70 sm:opacity-100"
    >

    <img 
      src="@/assets/svg/pic/metal_star.webp" 
      alt="metal_star" 
      class="absolute top-40 sm:top-52 md:top-70 left-4 sm:left-12 md:left-25 w-16 sm:w-24 md:w-1/5 max-w-[120px] md:max-w-none pointer-events-none hidden sm:block"
    >

    <div class="absolute top-1/6 sm:top-2/12 -right-10 sm:-right-30 w-40 sm:w-80 md:w-120 h-1.5 sm:h-2 bg-[#ff0000] opacity-20 blur-sm animate-pulse rotate-45 pointer-events-none"></div>

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
