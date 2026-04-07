<template>
  <!-- ОСНОВНОЙ КОНТЕЙНЕР: Стиль "Заблокированный терминал" -->
  <div class="min-h-screen flex items-center justify-center bg-black text-white px-4 font-['Impact','Arial_Black',sans-serif] selection:bg-[#39FF14] selection:text-black overflow-hidden relative">
    
    <!-- ФОН: Сканлайны, шум и "битые пиксели" -->
    <div class="absolute inset-0 z-0 bg-[url('https://www.transparenttextures.com/patterns/carbon-fibre.png')] opacity-20 pointer-events-none"></div>
    <div class="absolute inset-0 z-0 bg-[linear-gradient(rgba(18,16,16,0)_50%,rgba(0,0,0,0.25)_50%),linear-gradient(90deg,rgba(255,0,0,0.06),rgba(0,255,0,0.02),rgba(0,0,255,0.06))] bg-size-[100%_4px,3px_100%] pointer-events-none opacity-40"></div>

    <!-- Декоративные провода по углам экрана -->
    <div class="absolute top-0 left-1/4 w-0.5 h-32 bg-[#333] shadow-[0_0_10px_#ff0000]"></div>
    <div class="absolute bottom-0 right-1/4 w-0.5 h-32 bg-[#333] shadow-[0_0_10px_#39FF14]"></div>

    <!-- ФОРМА: Системная консоль -->
    <form 
      @submit.prevent="handleSubmit" 
      class="relative w-full max-w-lg bg-[#0a0a0a] border-[6px] border-[#333] p-0 shadow-[30px_30px_0_rgba(0,0,0,0.8)] flex flex-col group overflow-hidden"
    >
      <!-- HEADER БАР: Стиль "Security Access" -->
      <div class="bg-[#333] p-3 flex justify-between items-center border-b-4 border-black">
        <div class="flex items-center gap-3 px-2">
          <div class="w-3 h-3 bg-[#ff0000] animate-led shadow-[0_0_10px_#ff0000]"></div>
          <span class="text-sm font-mono text-gray-300 tracking-[0.3em] uppercase italic">SYSTEM_AUTH_V.03 // SECURE_UPLINK</span>
        </div>
        <div class="flex gap-1">
          <div class="w-4 h-4 bg-black/50"></div>
          <div class="w-4 h-4 bg-[#ff0000]/20"></div>
        </div>
      </div>

      <!-- ВНУТРЕННИЙ КОНТЕНТ -->
      <div class="p-8 md:p-12 space-y-8 bg-[url('https://www.transparenttextures.com/patterns/black-linen.png')] relative">
        
        <!-- ЛОГОТИП: Хром + Глитч -->
        <div class="text-center relative">
          <h1 class="text-7xl md:text-8xl tracking-tight uppercase leading-[0.8] transform scale-y-125 mb-2">
            <span class="text-transparent bg-clip-text bg-linear-to-b from-white via-gray-400 to-black drop-shadow-[4px_4px_0_#39FF14]">CLASS</span><br>
            <span class="text-[#39FF14] drop-shadow-[4px_4px_0_#000]">TICKETS</span>
          </h1>
          <div class="h-1 w-full bg-[#333] mt-4 relative overflow-hidden">
            <div class="absolute inset-0 bg-[#39FF14] w-1/4 animate-signal"></div>
          </div>
          <p class="text-sm font-mono text-gray-500 uppercase tracking-[0.5em] mt-4 italic">ARTIST_RESTRICTED_AREA</p>
        </div>

        <!-- ПОЛЯ ВВОДА: "Вдавленные" слоты -->
        <div class="space-y-6">
          <div class="flex flex-col gap-2 group/input">
            <label class="text-sm uppercase tracking-[0.4em] text-[#39FF14] font-mono  flex items-center gap-2">
              <span class="w-1.5 h-1.5 bg-[#39FF14]"></span> EMAIL_ADDRESS
            </label>
            <div class="relative">
              <input
                v-model="email"
                type="email"
                required
                :disabled="authStore.isLoading"
                class="w-full px-6 py-4 bg-black border-2 border-[#333] text-white font-mono text-lg focus:outline-none focus:border-[#39FF14] focus:shadow-[0_0_15px_rgba(57,255,20,0.2)] shadow-[inset_0_4px_10px_rgba(0,0,0,1)] transition-none placeholder:text-gray-800 uppercase"
                placeholder="ID@LABEL.SOX"
              />
              <div class="absolute right-4 top-1/2 -translate-y-1/2 text-sm font-mono text-gray-700 pointer-events-none">_CHIP_01</div>
            </div>
          </div>

          <div class="flex flex-col gap-2 group/input">
            <label class="text-sm uppercase tracking-[0.4em] text-[#39FF14] font-mono  flex items-center gap-2">
              <span class="w-1.5 h-1.5 bg-[#39FF14]"></span> ACCESS_KEY
            </label>
            <div class="relative">
              <input
                v-model="password"
                type="password"
                required
                :disabled="authStore.isLoading"
                class="w-full px-6 py-4 bg-black border-2 border-[#333] text-white font-mono text-lg focus:outline-none focus:border-[#39FF14] focus:shadow-[0_0_15px_rgba(57,255,20,0.2)] shadow-[inset_0_4px_10px_rgba(0,0,0,1)] transition-none placeholder:text-gray-800 uppercase"
                placeholder="********"
              />
              <div class="absolute right-4 top-1/2 -translate-y-1/2 text-sm font-mono text-gray-700 pointer-events-none">_CHIP_02</div>
            </div>
          </div>
        </div>

        <!-- ОШИБКА: Стиль "Critical Failure" -->
        <div v-if="error" class="bg-[#ff0000] text-black p-4  uppercase text-xs italic flex items-center gap-3 animate-strobe border-4 border-black">
          <span class="text-2xl">[!]</span>
          <div>
            <p>CRITICAL_ERROR: AUTH_FAILED</p>
            <p class="font-mono text-sm opacity-80">{{ error }}</p>
          </div>
        </div>

        <!-- КНОПКА ВХОДА: Массивный переключатель -->
        <button
          type="submit"
          :disabled="authStore.isLoading"
          class="group relative w-full bg-[#39FF14] text-black  uppercase py-6 border-4 border-black shadow-[8px_8px_0_#fff] hover:shadow-none hover:translate-x-1 hover:translate-y-1 active:translate-x-2 active:translate-y-2 transition-none disabled:opacity-50 overflow-hidden"
        >
          <div class="relative z-10 flex items-center justify-center gap-4 text-2xl italic tracking-tighter">
            <span v-if="!authStore.isLoading">INITIATE_LOGIN</span>
            <span v-else class="flex items-center gap-3">
              <!-- Спиннер как вращающийся CD -->
              <div class="w-6 h-6 border-4 border-black border-t-transparent rounded-full animate-spin"></div>
              UPLOADING...
            </span>
          </div>
          <!-- Глитч-полоса при ховере -->
          <div class="absolute inset-0 bg-white opacity-0 group-hover:opacity-20 animate-pulse pointer-events-none"></div>
        </button>

        <!-- FOOTER: Техническая пометка -->
        <div class="text-center pt-4 border-t-2 border-dashed border-[#222]">
           <div class="text-[9px] font-mono text-gray-600 uppercase tracking-widest flex justify-between items-center">
             <span>ENCRYPTION: AES_256</span>
             <span class="text-white">DEMO_MODE: ENABLED</span>
           </div>
           <p class="text-[8px] font-mono text-gray-800 mt-2 italic">BY_SOX_HEAVY_INDUSTRIES_2003</p>
        </div>
      </div>
    </form>
  </div>
</template>

<style scoped>
/* Анимация мигающего LED (из прошлого сета) */
@keyframes real-port-flicker {
  0%, 100% { opacity: 1; filter: drop-shadow(0 0 8px #ff0000); }
  2%, 6% { opacity: 0.1; filter: none; }
  4%, 8% { opacity: 1; filter: drop-shadow(0 0 10px #ff0000); }
  42% { opacity: 0; filter: none; }
  43% { opacity: 1; }
  88% { opacity: 0.1; }
  89% { opacity: 1; }
}
.animate-led {
  animation: real-port-flicker 4s infinite steps(1);
}

/* Бегущий сигнал в разделителе */
@keyframes signal-flow {
  0% { transform: translateX(-100%); }
  100% { transform: translateX(400%); }
}
.animate-signal {
  animation: signal-flow 2s infinite linear;
}

/* Стробоскоп для ошибки */
@keyframes strobe {
  0%, 100% { background-color: #ff0000; color: #000; }
  50% { background-color: #000; color: #ff0000; }
}
.animate-strobe {
  animation: strobe 0.2s infinite steps(1);
}

/* Эффект CRT монитора */
.min-h-screen::after {
  content: "";
  position: absolute;
  inset: 0;
  background-image: url("data:image/svg+xml,%3Csvg viewBox='0 0 200 200' xmlns='http://www.w3.org/2000/svg'%3Ffilter id='n'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='.65'/%3E%3C/filter%3E%3Crect width='100%25' height='100%25' filter='url(%23n)' opacity='.03'/%3E%3C/svg%3E");
  pointer-events: none;
  z-index: 50;
}
</style>


<script lang="ts" setup>
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
    error.value = err.message || 'Ошибка входа'
  }
}
</script>