<template>
  <div class="flex flex-1 items-center justify-center text-white p-7 font-['Inter',sans-serif] selection:bg-[#ff0000] selection:text-white overflow-hidden relative">
    
    <div class="bg-chain-placeholder absolute w-[120%] h-16 bg-repeat-x bg-center bg-size-[auto_100%] rotate-25 -right-30 top-2/4 z-10 mix-blend-screen pointer-events-none"></div>
    <div class="bg-chain-placeholder absolute w-[120%] h-16 bg-repeat-x bg-center bg-size-[auto_100%] -rotate-12 -left-10 bottom-1/4 z-10  mix-blend-screen pointer-events-none"></div>

    <form 
      @submit.prevent="handleSubmit" 
      class="relative w-full max-w-3xl bg-black border border-white/20 p-0 shadow-[0_40px_80px_rgba(0,0,0,0.7)] z-20 overflow-hidden"
    >
      <!-- HEADER -->
      <div class=" bg-white/20 text-black p-2 flex justify-between items-center">
        <div class="flex items-center gap-3">
          <div class="w-3 h-3 bg-[#ff0000] animate-pulse"></div>
          <span class="text-[10px] font-['JetBrains_Mono',monospace] font-black uppercase tracking-widest italic">
            AUTH_PROTOCOL // SECURITY_LEVEL: RED
          </span>
        </div>
        <span class="text-[10px] font-['JetBrains_Mono',monospace] opacity-50 uppercase">V.2026.03</span>
      </div>

      <!-- ВНУТРЕННИЙ КОНТЕНТ -->
      <div class="p-6 md:p-10 relative">
        
        <!-- ЛОГОТИП: Используем ваш стиль с коррекцией -->
        <div class="mb-8 relative text-center">
           <h1 class="h1-metal-textured text-6xl md:text-7xl m-0 leading-[0.8]" data-text="CLASS TICKETS">
             CLASS TICKETS
           </h1>
           <div class="mt-6 flex justify-center items-center gap-2">
              <div class="h-px w-12 bg-[#ff0000]"></div>
              <span class="text-[8px] font-['JetBrains_Mono',monospace] text-gray-500 uppercase tracking-[0.6em]">Artist_Terminal</span>
              <div class="h-px w-12 bg-[#ff0000]"></div>
           </div>
        </div>

        <!-- ПОЛЯ ВВОДА -->
        <div class="space-y-10">
          <!-- EMAIL -->
          <div class="relative group/input">
            <label class="absolute -top-3 left-4 bg-black px-2 text-xs font-['JetBrains_Mono',monospace] text-[#ff0000] uppercase tracking-widest z-20">
              User_ID
            </label>
            <input
              v-model="email"
              type="email"
              required
              class="w-full bg-transparent border-2 border-white/10 p-3 font-['Archivo_Black',sans-serif] text-xl focus:outline-none focus:border-[#ff0000] transition-colors placeholder:opacity-10 uppercase tracking-tighter"
              placeholder="YOUR_IDENTIFIER"
            />
            <div class="absolute bottom-0 right-0 w-4 h-4 border-r-2 border-b-2 border-[#ff0000] group-focus-within/input:w-full transition-all"></div>
          </div>

          <!-- PASSWORD -->
          <div class="relative group/input">
            <label class="absolute -top-3 left-4 bg-black px-2 text-xs font-['JetBrains_Mono',monospace] text-[#ff0000] uppercase tracking-widest z-20">
              Access_Key
            </label>
            <input
              v-model="password"
              type="password"
              required
              class="w-full bg-transparent border-2 border-white/10 p-3 font-['Archivo_Black',sans-serif] text-xl focus:outline-none focus:border-[#ff0000] transition-colors placeholder:opacity-10 uppercase tracking-tighter"
              placeholder="••••••••"
            />
            <div class="absolute bottom-0 right-0 w-4 h-4 border-r-2 border-b-2 border-[#ff0000] group-focus-within/input:w-full transition-all"></div>
          </div>
        </div>

        <!-- ERROR MESSAGE (с animate-ping) -->
        <div v-if="error" class="mt-8 bg-[#ff0000]/10 border-2 border-[#ff0000] text-white p-4 font-['Archivo_Black',sans-serif] uppercase text-xs flex items-center gap-4">
          <div class="relative flex h-5 w-5 items-center justify-center">
             <span class="absolute inline-flex h-full w-full animate-ping rounded-full bg-[#ff0000] opacity-75"></span>
             <span class="relative inline-flex h-3 w-3 items-center justify-center rounded-full bg-[#ff0000] text-black text-xs font-black">!</span>
          </div>
          <div class="leading-none tracking-tighter">
            Access_Denied: {{ error }}
          </div>
        </div>

        <!-- SUBMIT BUTTON -->
        <div class="mt-14 relative group">
            <button
              type="submit"
              :disabled="authStore.isLoading"
              class="relative w-full bg-white text-black font-['Archivo_Black',sans-serif] text-2xl uppercase py-3 transition-all hover:bg-[#ff0000] hover:text-white overflow-hidden disabled:opacity-30 z-10"
            >
              <span class="relative z-10 flex items-center justify-center gap-4">
                {{ authStore.isLoading ? 'Processing...' : 'Enter_System' }}
                <span class="text-sm">>>></span>
              </span>
              <div class="absolute inset-0 crt-noise opacity-20 pointer-events-none"></div>
            </button>
            <div class="absolute inset-0 bg-white/20 translate-x-2 translate-y-2 -z-10 group-hover:translate-x-0 group-hover:translate-y-0 transition-transform"></div>
        </div>
      </div>
    </form>
  </div>
</template>

<style scoped>
/* СТИЛЬ ДЛЯ ЦЕПЕЙ (из вашего примера) */
.bg-chain-placeholder {
    background-image: url("@/assets/chrome/chain_bg.png");
}
.bg-size-\[auto_100\%\] {
  background-size: auto 100%;
}

/* КОРРЕКЦИЯ ДЛЯ ВАШЕГО h1-metal-textured ПОД ШРИФТ Archivo Black */
.h1-metal-textured {
  font-family: 'Archivo Black', 'Impact', sans-serif;
  letter-spacing: -0.05em; /* Делаем буквы плотнее */
  padding-right: 0; /* Убираем лишний отступ */
}
/* Смещаем блик ниже, чтобы он попадал на массивные буквы Archivo Black */
.h1-metal-textured::after {
  top: 2rem;
  animation: metal-shine 6s linear infinite; /* Ускоряем анимацию */
}

/* СЕТКА */
.y2k-bg-grid {
  background-size: 24px 24px;
  background-image: radial-gradient(circle, #222 1px, transparent 1px);
}

/* ШУМ */
.crt-noise {
  background-image: url('data:image/svg+xml;utf8,%3Csvg viewBox="0 0 200 200" xmlns="http://www.w3.org/2000/svg"%3E%3Cfilter id="noiseFilter"%3E%3CfeTurbulence type="fractalNoise" baseFrequency="0.9" numOctaves="3" stitchTiles="stitch"/%3E%3C/filter%3E%3Crect width="100%25" height="100%25" filter="url(%23noiseFilter)"/%3E%3C/svg%3E');
}
</style>

<script lang="ts" setup>
// Ваш JS-код остается без изменений
import { useAuthStore } from '@/stores/auth'
import { useRouter } from 'vue-router'
import { ref } from 'vue'

const authStore = useAuthStore()
const router = useRouter()
const email = ref('')
const password = ref('')
const error = ref('')

async function handleSubmit() {
  try {
    error.value = ''
    const success = await authStore.login(email.value, password.value)
    if (success) {
      router.push('/dashboard')
    }
  } catch (err: any) {
    error.value = err.message || 'AUTH_FAILURE'
  }
}
</script>