<template>
  <footer class="relative bg-black border-t-4 border-[#333] font-['Impact','Arial_Black',sans-serif] overflow-hidden pb-[env(safe-area-inset-bottom)]">
    <div class="max-w-7xl mx-auto grid grid-cols-1 md:grid-cols-2 lg:grid-cols-12 items-stretch">
      
      <!-- Brand -->
      <div class="lg:col-span-3 p-3 sm:p-4 border-b md:border-b-0 md:border-r border-[#222] flex items-center gap-3 sm:gap-4 bg-[#0a0a0a]">
        <div class="w-14 h-14 sm:w-20 sm:h-20 border-2 border-[#39FF14] relative overflow-hidden shrink-0 shadow-[3px_3px_0_#ff0000] sm:shadow-[4px_4px_0_#ff0000] bg-[#111] flex items-center justify-center">
          <span class="text-[#39FF14] text-xl sm:text-2xl font-black italic">CT</span>
          <div class="absolute inset-0 bg-[#39FF14]/10 mix-blend-overlay pointer-events-none"></div>
        </div>
        <div class="group cursor-default min-w-0">
          <h3 class="text-xl sm:text-3xl md:text-4xl leading-[0.85] tracking-tighter uppercase italic">
            <span class="text-white block group-hover:text-[#ff0000]">CLASS</span>
            <span class="text-[#39FF14] block drop-shadow-[2px_2px_0_#000]">TICKETS</span>
          </h3>
          <p class="text-[9px] font-mono text-gray-500 mt-1 sm:mt-2">ENCRYPTED_BY_.SOX</p>
        </div>
      </div>

      <!-- Quick menu — only real routes -->
      <div class="lg:col-span-6 bg-[#39FF14] p-2 sm:p-3 border-b lg:border-b-0 lg:border-r border-black">
        <div class="mb-1 sm:mb-2">
          <span class="text-black text-sm sm:text-xl md:text-2xl font-black bg-white px-1 border border-black italic">QUICK_MENU:</span>
        </div>
        <nav class="grid grid-cols-2 sm:flex sm:flex-wrap gap-1 sm:gap-x-4 sm:gap-y-1" aria-label="Footer">
          <router-link
            v-for="(link, index) in links"
            :key="link.to"
            :to="link.to"
            class="group flex items-center gap-1 text-black text-sm sm:text-lg md:text-xl font-black hover:bg-black hover:text-[#39FF14] px-1 py-1.5 sm:py-0 min-h-[44px] sm:min-h-0"
          >
            <span class="text-[10px] sm:text-sm md:text-lg bg-black text-[#39FF14] px-1 group-hover:bg-[#ff0000] group-hover:text-white shrink-0">0{{ index + 1 }}</span>
            <span class="truncate">{{ link.label }}</span>
          </router-link>
        </nav>
      </div>

      <!-- Meta -->
      <div class="lg:col-span-3 p-3 sm:p-4 bg-[#050505] flex flex-col justify-center relative md:col-span-2 lg:col-span-3">
        <div class="absolute inset-0 bg-[radial-gradient(#222_1px,transparent_1px)] bg-size-[4px_4px] opacity-30 pointer-events-none"></div>
        <div class="relative z-10 flex flex-col gap-1">
          <div class="flex justify-between text-[10px] font-mono text-gray-400 gap-2">
            <span>©{{ currentYear }} .SOX_CORE</span>
            <span class="text-[#ff0000] motion-safe:animate-pulse">● LIVE</span>
          </div>
          <div class="h-5 w-full bg-[#222] border border-[#333] flex items-center justify-center">
            <span class="font-mono text-[8px] text-gray-500 tracking-widest">||||||||||||||||||||||||</span>
          </div>
          <p class="text-[8px] font-mono text-gray-600 text-center uppercase tracking-[0.15em]">All rights destroyed</p>
        </div>
      </div>
    </div>

    <div class="bg-black border-t border-[#222] py-1 flex items-center overflow-hidden whitespace-nowrap relative">
      <div class="flex-1 overflow-hidden relative">
        <div class="flex motion-safe:animate-marquee text-[9px] font-mono text-[#333] uppercase">
          <div class="flex gap-4 px-2">
            <span v-for="i in 8" :key="'a' + i">System.Initialize... OK // CLASS_TICKETS // .SOX_OS //</span>
          </div>
        </div>
        <div class="absolute inset-y-0 right-0 w-12 bg-linear-to-l from-black to-transparent z-10 pointer-events-none"></div>
      </div>
      <div class="relative z-20 shrink-0 ml-2 sm:ml-4 bg-[#111] px-2 border border-[#333] text-[#39FF14] text-[9px] font-mono">
        V.03_BETA
      </div>
    </div>
  </footer>
</template>

<style scoped>
@keyframes marquee {
  0% { transform: translateX(0); }
  100% { transform: translateX(-50%); }
}
.animate-marquee {
  display: flex;
  width: max-content;
  animation: marquee 30s linear infinite;
}
@media (prefers-reduced-motion: reduce) {
  .animate-marquee { animation: none; }
}
</style>

<script lang="ts">
export default {
  name: 'Footer',
  data() {
    return {
      currentYear: new Date().getFullYear(),
      links: [
        { to: '/', label: 'HOME' },
        { to: '/about', label: 'ABOUT' },
        { to: '/cases', label: 'CASES' },
        { to: '/news', label: 'NEWS' },
        { to: '/events', label: 'EVENTS' },
        { to: '/guides', label: 'GUIDES' },
        { to: '/login', label: 'LOGIN' },
      ],
    }
  },
}
</script>
