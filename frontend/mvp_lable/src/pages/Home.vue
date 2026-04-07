<template>
  <!-- Главный контейнер: Кастомный курсор-прицел, жесткий черный фон, сетка и сканлайны -->
  <div class="relative flex-1 overflow-hidden w-full grid grid-cols-2 lg:grid-cols-4">

      <!-- ЦЕНТРАЛЬНЫЙ БЛОК: Агрессивная типографика и CTA -->
      <div class="col-span-1 lg:col-span-2 flex flex-col justify-center relative">

        <!-- Заголовок: Хром + Неон -->
        <div class="relative z-10 transform">

          <h1 class="relative z-20">
            <span class="block text-transparent bg-clip-text bg-linear-to-b from-white via-gray-300 to-gray-700 drop-shadow-[2px_2px_0_#39FF14]">
              CL4SS
            </span>
            <span class="block text-[#39FF14] drop-shadow-[2px_2px_0_#fff] pb-2">
              T1CK3T$
            </span>
          </h1>
          <!-- y2k stars -->
          <img src="@/assets/svg/y2k/stars.svg" alt="y2k_start" class="absolute z-18 -top-5 left-30 w-90 pointer-events-none select-none drop-shadow-[2px_2px_0_#fff]">
        </div>

        <!-- Главная кнопка: Никаких плавных транзишенов, только удар -->
        <router-link to="/purchase"
          class="block z-10 bg-[#39FF14] text-black w-100 border-4 border-black font-black text-4xl p-6 text-center uppercase
          hover:bg-black hover:text-[#39FF14] hover:border-[#39FF14] shadow-[8px_8px_0_#ff0000] hover:shadow-[-8px_-8px_0_#39FF14]
          active:translate-y-2 active:translate-x-2 active:shadow-none transition-none relative overflow-hidden group mt-10">

          <span class="relative flex items-center justify-center gap-4]">
            <span class="text-red-600 text-3xl">✖</span> PURCHASE_ACCESS
          </span>

          <!-- Глитч-вспышка при наведении -->
          <div class="absolute inset-0 bg-white opacity-0 group-hover:opacity-20 group-hover:animate-ping pointer-events-none"></div>

        </router-link>

               <!-- Текст: Терминальный лог -->
        <!-- <div class=" absolute bg-black border border-[#39FF14] p-4 font-mono text-sm text-[#39FF14] my-6 bottom-0 w-full">
          <div class="absolute top-0 left-0 w-full h-full bg-[#39FF14] opacity-10 animate-pulse pointer-events-none"></div>
          <p class="leading-tight">
            > INITIALIZING... <br>
            > URBAN_STREET_ENERGY: LOADED.<br>
            > ERROR: TOO MUCH SWAG DETECTED.<br>
            Быстрая покупка классов и пакетов. Зеленые билеты. Мы не делаем красиво, мы делаем громко.
          </p>
        </div> -->

      </div>


      <!-- yk2 star -->
<!--      <img src="@/assets/svg/y2k/b_star.svg" alt="y2k_l_moon" class="absolute z-10 w-1/2 -top-70 -right-60 -rotate-30 blur-sm pointer-events-none">-->

      <!-- yk2 disc -->
       <img src="@/assets/svg/pic/disc.svg" alt="y2k_l_moon" class="absolute w-3/5 -top-1/3 -right-40 opacity-40 blur-[1px] mix-blend-overlay animate-spin-slow pointer-events-none" >

      <img src="@/assets/watermark-class-tickets.png" alt="" class="pointer-events-none opacity-5 absolute bottom-0 left-20">

      <!-- ПРАВЫЙ БЛОК: Изображения / Визуальный мусор 4:3 -->
      <div class="col-span-3 lg:col-span-2 lg:col-start-3 relative p-6 flex items-center justify-center overflow-hidden">


        <!-- Контейнер для фото 4:3 (Слот для арта) -->
        <div class="w-full h-full relative shadow-[10px_10px_0_#000] group z-20">
            <img
              src="@/assets/svg/face/kai.png"
              alt="vhs-effect"
              class="absolute inset-0 w-full h-full object-cover blur-[1px] select-none pointer-events-none"
            />
          <!-- Рамка записи видеокамеры -->
<!--          <div class="absolute top-0 left-0 w-4 h-4 border-t-4 border-l-4 border-red-500"></div>-->
<!--          <div class="absolute top-0 right-0 w-4 h-4 border-t-4 border-r-4 border-red-500"></div>-->
<!--          <div class="absolute bottom-0 left-0 w-4 h-4 border-b-4 border-l-4 border-red-500"></div>-->
<!--          <div class="absolute bottom-0 right-0 w-4 h-4 border-b-4 border-r-4 border-red-500"></div>-->

<!--          <div class="absolute top-4 left-4 text-red-500 font-mono text-ls flex items-center gap-2 animate-pulse">-->
<!--            <div class="w-3 h-3 bg-red-500 rounded-full"></div> REC-->
<!--          </div>-->
        </div>
      </div>
    </div>
</template>

<style scoped>
/* Кастомные анимации и эффекты, которые невозможно или нецелесообразно делать через inline Tailwind */

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

/* Грязное выделение текста */
::selection {
  background: #39FF14;
  color: #000;
  text-shadow: none;
}
</style>

<script setup lang="ts">
import LineIcon from '@/assets/svg/line.svg'
</script>
