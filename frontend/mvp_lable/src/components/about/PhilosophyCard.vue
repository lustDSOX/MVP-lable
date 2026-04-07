<template>
  <div 
    class="relative group overflow-hidden border-2 border-[#222] bg-black p-6 transition-all duration-300 hover:border-[#39FF14]/50"
  >
    <!-- 1. Фоновая текстура (Сканлайны) -->
    <div class="absolute inset-0 pointer-events-none opacity-100 bg-[linear-gradient(rgba(18,16,16,0)_50%,rgba(0,0,0,0.25)_50%),linear-gradient(90deg,rgba(255,0,0,0.06),rgba(0,255,0,0.02),rgba(0,0,255,0.06))] bg-size-[100%_20px,20px_100%]"></div>

    <!-- 2. Декоративные уголки (Brutalism style) -->
    <div class="absolute top-0 left-0 w-2 h-2 border-t-2 border-l-2 border-[#333] group-hover:border-[#39FF14]"></div>
    <div class="absolute bottom-0 right-0 w-2 h-2 border-b-2 border-r-2 border-[#333] group-hover:border-[#39FF14]"></div>

    <!-- 3. Техническая инфо-строка сверху -->
    <div class="flex justify-between items-center mb-8">
      <div class="flex gap-1">
        <div class="w-1 h-3 bg-[#39FF14] animate-pulse"></div>
        <span class="text-[10px] font-mono text-[#444] group-hover:text-[#39FF14]">SEC_00{{ item.id }}</span>
      </div>
      <span class="text-[10px] font-mono text-[#444]">STATUS: ACTIVE</span>
    </div>

    <!-- 4. Основной текст -->
    <div class="relative z-10">
      <h3 class="text-2xl md:text-3xl italic uppercase leading-none mb-2 group-hover:text-[#39FF14] transition-colors">
        {{ item.text }}
      </h3>
      <!-- Декоративный штрих-код или паттерн -->
      <div class="w-full h-1 bg-[#1a1a1a] mt-4 flex gap-1">
        <div v-for="n in 12" :key="n" :class="['h-full w-full bg-[#222] group-hover:bg-[#39FF14]/20', n % 3 === 0 ? 'opacity-0' : '']"></div>
      </div>
    </div>

    <!-- 5. Фоновый ID -->
    <div class="absolute -right-4 -bottom-6 text-9xl  italic text-white opacity-[0.02] group-hover:opacity-[0.05] group-hover:-rotate-12 transition-all duration-700 select-none">
      0{{ item.id }}
    </div>

    <!-- 6. Эффект наведения -->
    <div class="absolute inset-0 bg-[#39FF14] opacity-0 group-hover:opacity-[0.03] pointer-events-none transition-opacity"></div>
  </div>
</template>

<script lang="ts">

export default {
  name: 'PhilosophyCard',
  props: {
    item: {
      type: Object,
      required: true,
      default: () => ({ id: 1, text: 'DEFAULT_TEXT' })
    }
  }
}
</script>

<style scoped>
/* Добавляем легкое дрожание при наведении */
.group:hover h3 {
  animation: glitch 0.3s infinite;
}
</style>