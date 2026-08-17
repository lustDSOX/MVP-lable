<template>
  <section class="flex-1 flex flex-col items-center justify-center px-4 py-16 sm:py-24 text-center relative overflow-hidden">
    <div class="relative z-10 max-w-lg w-full border-4 border-black bg-[#0a0a0a] shadow-[8px_8px_0_#39FF14] p-6 sm:p-10">
      <p class="font-mono text-[10px] sm:text-xs text-[#39FF14] tracking-widest mb-3">SYSTEM // ACCESS_GATE</p>
      <h1 class="text-3xl sm:text-5xl font-black uppercase italic text-white mb-4 leading-none">
        PURCHASE<br />
        <span class="text-[#39FF14]">SOON</span>
      </h1>
      <p class="font-mono text-sm text-gray-400 mb-8 leading-relaxed">
        Module under construction. Tickets &amp; label packs will open here.
      </p>
      <router-link
        to="/"
        class="inline-block w-full sm:w-auto bg-[#39FF14] text-black border-4 border-black font-black text-lg sm:text-xl px-6 py-3 uppercase shadow-[4px_4px_0_#ff0000] hover:bg-black hover:text-[#39FF14] hover:border-[#39FF14] active:translate-x-1 active:translate-y-1 active:shadow-none"
      >
        ← BACK_HOME
      </router-link>
    </div>
  </section>
</template>

<script lang="ts">
export default { name: 'PurchaseStub' }
</script>
