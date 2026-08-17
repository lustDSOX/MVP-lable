<template>
  <!-- Главный контейнер -->
  <div class="relative flex-1 overflow-hidden w-full max-w-[100vw] grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 min-h-[70vh]">

      <!-- ЦЕНТРАЛЬНЫЙ БЛОК -->
      <div class="col-span-1 lg:col-span-2 p-4 sm:p-6 flex flex-col justify-center relative order-1">

        <div class="relative z-10 transform">
          
          <h1 class="text-4xl sm:text-5xl md:text-6xl lg:text-8xl">
            <span class="block text-transparent bg-clip-text bg-linear-to-b from-white via-gray-300 to-gray-700 drop-shadow-[2px_2px_0_#39FF14]">
              CL4SS
            </span>
            <span class="block text-[#39FF14] drop-shadow-[2px_2px_0_#fff] pb-2 relative">
              <img 
                src="@/assets/svg/y2k/stars.svg" 
                alt="y2k_start" 
                class="z-20 absolute -top-8 sm:-top-12 md:-top-16 lg:-top-20 left-4 sm:left-10 md:left-16 lg:left-26 w-24 sm:w-40 md:w-56 lg:w-70 max-w-[40vw] pointer-events-none select-none hidden sm:block"
              >
              T1CK3T$
            </span>
          </h1>
        </div>

        <router-link to="/purchase" 
          class="block z-10 bg-[#39FF14] text-black border-4 border-black font-black text-xl sm:text-2xl md:text-3xl lg:text-4xl p-4 sm:p-5 md:p-6 text-center uppercase 
          hover:bg-black hover:text-[#39FF14] hover:border-[#39FF14] shadow-[8px_8px_0_#ff0000] hover:shadow-[-8px_-8px_0_#39FF14] 
          active:translate-y-2 active:translate-x-2 active:shadow-none transition-none relative overflow-hidden group mt-6 sm:mt-10">

          <span class="relative flex items-center justify-center gap-2 sm:gap-4">
            <span class="text-red-600 text-2xl sm:text-3xl">✖</span> PURCHASE_ACCESS
          </span>

          <div class="absolute inset-0 bg-white opacity-0 group-hover:opacity-20 group-hover:animate-ping pointer-events-none"></div>

        </router-link>
      </div>

      <img 
        src="@/assets/svg/y2k/b_star.svg" 
        alt="y2k_star" 
        class="absolute z-10 w-[60%] sm:w-1/2 max-w-[280px] sm:max-w-none -top-20 sm:-top-40 md:-top-56 lg:-top-70 -right-16 sm:-right-32 md:-right-48 lg:-right-60 -rotate-30 blur-sm pointer-events-none opacity-60 sm:opacity-100"
      >

      <img 
        src="@/assets/watermark-class-tickets.png" 
        alt="" 
        class="pointer-events-none opacity-5 absolute bottom-0 left-4 sm:left-10 md:left-20 max-w-[80%] sm:max-w-none h-auto"
      >

      <div class="col-span-1 lg:col-span-1 lg:col-start-4 relative p-4 sm:p-6 flex items-center justify-center overflow-hidden order-2">

        <div class="w-full max-w-md mx-auto aspect-4/3 relative shadow-[6px_6px_0_#000] sm:shadow-[10px_10px_0_#000] group z-20">
            <!-- Mobile: no 1.3MB GIF — static VHS panel -->
            <div
              class="md:hidden absolute inset-0 m-1.5 bg-[#0a0a0a] flex flex-col items-center justify-center gap-2 select-none pointer-events-none"
              aria-hidden="true"
            >
              <div class="w-full h-full absolute inset-0 opacity-30 bg-[repeating-linear-gradient(0deg,transparent,transparent_2px,rgba(0,0,0,0.4)_2px,rgba(0,0,0,0.4)_4px)]"></div>
              <span class="relative font-mono text-[10px] text-red-500 tracking-widest">NO_SIGNAL // MOBILE</span>
            </div>
            <!-- Desktop: animated GIF -->
            <img 
              v-if="showHeroGif"
              src="@/assets/kai-angel-viperr.gif" 
              alt="vhs-effect" 
              loading="lazy" decoding="async"
              class="hidden md:block absolute inset-0 w-full h-full object-cover object-center p-2 blur-[1px] select-none pointer-events-none"
            />
          <div class="absolute top-0 left-0 w-3 h-3 sm:w-4 sm:h-4 border-t-2 sm:border-t-4 border-l-2 sm:border-l-4 border-red-500"></div>
          <div class="absolute top-0 right-0 w-3 h-3 sm:w-4 sm:h-4 border-t-2 sm:border-t-4 border-r-2 sm:border-r-4 border-red-500"></div>
          <div class="absolute bottom-0 left-0 w-3 h-3 sm:w-4 sm:h-4 border-b-2 sm:border-b-4 border-l-2 sm:border-l-4 border-red-500"></div>
          <div class="absolute bottom-0 right-0 w-3 h-3 sm:w-4 sm:h-4 border-b-2 sm:border-b-4 border-r-2 sm:border-r-4 border-red-500"></div>
          
          <div class="absolute top-2 sm:top-4 left-2 sm:left-4 text-red-500 font-mono text-xs sm:text-sm flex items-center gap-1.5 sm:gap-2 animate-pulse">
            <div class="w-2 h-2 sm:w-3 sm:h-3 bg-red-500 rounded-full"></div> REC
          </div>
        </div>
      </div>
    </div>
</template>

<style scoped>
.crt-overlay {
  background: linear-gradient(
    rgba(18, 16, 16, 0) 50%,
    rgba(0, 0, 0, 0.25) 50%
  ),
  linear-gradient(
    90deg,
    rgba(255, 0, 0, 0.06),
    rgba(0, 255, 0, 0.02),
    rgba(0, 0, 255, 0.06)
  );
  background-size: 100% 4px, 3px 100%;
}

@keyframes eq-bars {
  0% { height: 10%; }
  25% { height: 100%; }
  50% { height: 40%; }
  75% { height: 80%; }
  100% { height: 10%; }
}

.animate-eq {
  animation: eq-bars 0.8s infinite steps(4, end);
}

.animate-spin-slow {
  animation: spin 20s linear infinite;
}

@keyframes spin {
  from { transform: rotate(0deg); }
  to { transform: rotate(360deg); }
}

::selection {
  background: #39FF14;
  color: #000;
  text-shadow: none;
}
</style>

<script setup lang="ts">
import { ref, onMounted } from 'vue'

/** 1.3MB GIF only on desktop — mobile keeps static VHS panel */
const showHeroGif = ref(false)
onMounted(() => {
  showHeroGif.value = window.matchMedia('(min-width: 768px)').matches
})
</script>
