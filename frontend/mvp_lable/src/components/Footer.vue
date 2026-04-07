<template>
  <!-- ФУТЕР: Узкий, плотный, индустриальный -->
  <footer class="relative bg-black border-t-4 border-[#333] font-['Impact','Arial_Black',sans-serif] overflow-hidden">


    <div class="max-w-350 mx-auto grid grid-cols-1 lg:grid-cols-12 items-stretch">

      <!-- БЛОК 1: БРЕНДИНГ + GIF (Слева) -->
      <div class="lg:col-span-3 p-4 border-r-2 border-[#222] flex items-center gap-4 bg-[#0a0a0a]">
        <!-- GIF ЗАГЛУШКА: Стилизованный глитч-арт или логотип (4:3) -->
        <div class="w-24 h-24 border-2 border-[#39FF14] relative overflow-hidden shrink-0 shadow-[4px_4px_0_#ff0000]">
          <img src="https://media.giphy.com/media/v1.Y2lkPTc5MGI3NjExNHJqZnd4ZWZ4eHh4eHh4eHh4eHh4eHh4eHh4eHh4eHh4eHh4eHh4JmVwPXYxX2ludGVybmFsX2dpZl9ieV9pZCZjdD1n/6YfM6865H0U0mS5S2n/giphy.gif"
               class="w-full h-full object-cover grayscale contrast-200" alt="vibe">
          <div class="absolute inset-0 bg-[#39FF14]/20 mix-blend-overlay"></div>
        </div>

        <!-- Лого с тем самым ховером -->
        <div class="group cursor-default">
          <h3 class="text-4xl leading-[0.8] tracking-tighter uppercase italic transition-none">
            <span class="text-white block group-hover:text-[#ff0000]">CLASS</span>
            <span class="text-[#39FF14] block drop-shadow-[2px_2px_0_#000] group-hover:translate-x-1 transition-none">TICKETS</span>
          </h3>
          <p class="text-[9px] font-mono text-gray-500 mt-2">ENCRYPTED_BY_.SOX</p>
        </div>
      </div>

      <!-- БЛОК 2: QUICK_ACCESS (Центр) -->
      <!-- Высокий контраст, мелкий "TRK" -->
      <div class="lg:col-span-6 bg-[#39FF14] p-2 border-r-2 border-black flex flex-wrap items-center gap-x-6 gap-y-2">
        <div class="w-full mb-1">
          <span class="text-black text-3xl font-black bg-white px-1 border border-black italic">QUICK_MENU:</span>
        </div>

        <router-link v-for="(link, index) in [
            {to: '/', label: 'HOME'},
            {to: '/about', label: 'ABOUT'},
            {to: '/packages', label: 'PACKS'},
            {to: '/artists', label: 'ARTISTS'},
            {to: '/rules', label: 'RULES'}
          ]" :key="index"
          :to="link.to"
          class="group flex items-center gap-1 text-black text-2xl font-black hover:bg-black hover:text-[#39FF14] transition-none px-1">
          <span class="text-2xl bg-black text-[#39FF14] px-1 group-hover:bg-[#ff0000] group-hover:text-white">0 {{index+1}}</span>
          {{link.label}}
        </router-link>
      </div>

      <!-- БЛОК 3: ИНФО-МУСОР (Справа) -->
      <div class="lg:col-span-3 p-4 bg-[#050505] flex flex-col justify-center relative">
        <!-- Текстура сетки -->
        <div class="absolute inset-0 bg-[radial-gradient(#222_1px,transparent_1px)] bg-size-[4px_4px] opacity-30"></div>

        <div class="relative z-10 flex flex-col gap-1">
          <div class="flex justify-between text-[10px] font-mono text-gray-400">
            <span>©{{ currentYear }} .SOX_CORE</span>
            <span class="text-[#ff0000] animate-pulse">● LIVE_STREAM</span>
          </div>
          <!-- Штрих-код стал компактнее -->
          <div class="h-6 w-full bg-white mix-blend-screen opacity-50 grayscale invert">
            <img src="https://pngimg.com/uploads/barcode/barcode_PNG13.png" class="h-full w-full object-cover" alt="code">
          </div>
          <p class="text-[8px] font-mono text-gray-600 text-center uppercase tracking-[0.2em]">All rights destroyed</p>
        </div>
      </div>
    </div>

    <!-- ТЕХНИЧЕСКИЙ ПОДВАЛ-->
    <div class="bg-black border-t border-[#222] py-1  flex items-center overflow-hidden whitespace-nowrap relative">

      <div class="flex-1 overflow-hidden relative">
        <div class="flex animate-marquee text-[9px] font-mono text-[#333] uppercase">
          <!-- Блок-слайдер -->
          <div class="flex gap-4 px-2">
            <span v-for="i in 8" :key="'a' + i">System.Initialize... OK // Audio_Codec: LAME_V3 // Bitrate: Variable // User: Guest // .SOX_OS //</span>
          </div>
        </div>

        <!-- Градиентное затухание, чтобы текст плавно уходил "под" версию (опционально) -->
        <div class="absolute inset-y-0 right-0 w-16 bg-linear-to-l from-black to-transparent z-10"></div>
      </div>

      <!-- 2. БЛОК ВЕРСИИ (Pinned to right) -->
      <div class="relative z-20 shrink-0 ml-4 bg-[#111] px-2 border border-[#333] text-[#39FF14] text-[9px] font-mono shadow-[2px_2px_0_#000]">
        V.03_BETA
      </div>
    </div>
  </footer>
</template>

<style scoped>
@keyframes marquee-fast {
  0% { transform: translateX(0); }
  100% { transform: translateX(-20%); }
}

@keyframes marquee {
  0% { transform: translateX(0); }
  100% { transform: translateX(-50%); }
}
.animate-marquee {
  display: flex;
  width: max-content;
  animation: marquee 30s linear infinite;
}

h3:hover {
  text-shadow: 2px 0 #ff0000, -2px 0 #39FF14;
}
</style>

<script lang="ts">
export default {
  name: 'Footer',
  data() {
    return {
      currentYear: new Date().getFullYear(),
    }
  },
}
</script>
