<template>
  <div class="flex flex-1 items-center justify-center text-white p-4 sm:p-7 font-['Inter',sans-serif] selection:bg-[#ff0000] selection:text-white overflow-hidden relative">
    <div class="bg-chain-placeholder absolute w-[120%] h-16 bg-repeat-x bg-center bg-size-[auto_100%] rotate-25 -right-30 top-2/4 z-10 mix-blend-screen pointer-events-none hidden md:block"></div>

    <form
      @submit.prevent="handleSubmit"
      class="relative w-full max-w-3xl bg-black border border-white/20 p-0 shadow-[0_40px_80px_rgba(0,0,0,0.7)] z-20 overflow-hidden"
    >
      <div class="bg-white/20 text-black p-2 flex justify-between items-center">
        <div class="flex items-center gap-3">
          <div class="w-3 h-3 bg-[#ff0000] animate-pulse"></div>
          <span class="text-[10px] font-mono font-black uppercase tracking-widest italic">
            AUTH_PROTOCOL // {{ mode === 'login' ? 'LOGIN' : 'REGISTER' }}
          </span>
        </div>
        <span class="text-[10px] font-mono opacity-50 uppercase">MOCK</span>
      </div>

      <div class="p-6 md:p-10 relative">
        <div class="mb-6 relative text-center">
          <h1 class="h1-metal-textured text-5xl sm:text-6xl md:text-7xl m-0 leading-[0.8]" data-text="CLASS TICKETS">
            CLASS TICKETS
          </h1>
          <div class="mt-4 flex justify-center items-center gap-2">
            <div class="h-px w-12 bg-[#ff0000]"></div>
            <span class="text-[8px] font-mono text-gray-500 uppercase tracking-[0.4em]">Artist_Terminal</span>
            <div class="h-px w-12 bg-[#ff0000]"></div>
          </div>
        </div>

        <div class="flex gap-2 mb-8 border border-[#333] p-1">
          <button
            type="button"
            class="flex-1 py-2 text-xs font-mono uppercase tracking-widest transition-colors min-h-[44px]"
            :class="mode === 'login' ? 'bg-[#39FF14] text-black' : 'text-gray-500 hover:text-white'"
            @click="mode = 'login'; error = ''"
          >
            Login
          </button>
          <button
            type="button"
            class="flex-1 py-2 text-xs font-mono uppercase tracking-widest transition-colors min-h-[44px]"
            :class="mode === 'register' ? 'bg-[#39FF14] text-black' : 'text-gray-500 hover:text-white'"
            @click="mode = 'register'; error = ''"
          >
            Register
          </button>
        </div>

        <div class="space-y-8">
          <div v-if="mode === 'register'" class="relative">
            <label class="absolute -top-3 left-4 bg-black px-2 text-xs font-mono text-[#ff0000] uppercase tracking-widest z-20">Artist_Name</label>
            <input v-model="artistName" type="text" class="w-full bg-transparent border-2 border-white/10 p-3 font-mono text-white focus:border-[#39FF14] outline-none min-h-[48px]" placeholder="DJ Neon" />
          </div>
          <div class="relative">
            <label class="absolute -top-3 left-4 bg-black px-2 text-xs font-mono text-[#ff0000] uppercase tracking-widest z-20">User_ID</label>
            <input v-model="email" type="email" required class="w-full bg-transparent border-2 border-white/10 p-3 font-mono text-white focus:border-[#39FF14] outline-none min-h-[48px]" placeholder="demo@label.ru" />
          </div>
          <div class="relative">
            <label class="absolute -top-3 left-4 bg-black px-2 text-xs font-mono text-[#ff0000] uppercase tracking-widest z-20">Access_Key</label>
            <input v-model="password" type="password" required minlength="6" class="w-full bg-transparent border-2 border-white/10 p-3 font-mono text-white focus:border-[#39FF14] outline-none min-h-[48px]" placeholder="••••••••" />
          </div>
        </div>

        <p v-if="error" class="mt-4 text-[#ff0000] font-mono text-sm">{{ error }}</p>

        <button
          type="submit"
          :disabled="authStore.isLoading"
          class="mt-8 w-full bg-[#39FF14] text-black font-black text-lg sm:text-xl p-4 uppercase border-4 border-black shadow-[6px_6px_0_#ff0000] hover:bg-black hover:text-[#39FF14] hover:border-[#39FF14] transition-colors min-h-[52px] disabled:opacity-50"
        >
          {{ authStore.isLoading ? 'PROCESSING…' : mode === 'login' ? 'ENTER_SYSTEM' : 'CREATE_ARTIST' }}
        </button>

        <div class="mt-6 font-mono text-[10px] text-gray-600 uppercase space-y-1 leading-relaxed">
          <p>demo@label.ru / demo123 — artist</p>
          <p>moderator@label.ru / mod123 — only releases</p>
          <p>news@label.ru / news123 — only news CMS</p>
          <p>events@label.ru / events123 — only events CMS</p>
          <p>staff@label.ru / staff123 — releases+news+events</p>
          <p>admin@label.ru / admin123 — matrix + all</p>
        </div>
      </div>
    </form>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { useAuthStore } from '@/stores/auth'

const authStore = useAuthStore()
const router = useRouter()

const mode = ref<'login' | 'register'>('login')
const email = ref('')
const password = ref('')
const artistName = ref('')
const error = ref('')

async function handleSubmit() {
  error.value = ''
  try {
    if (mode.value === 'register') {
      await authStore.register(email.value, password.value, artistName.value)
    } else {
      await authStore.login(email.value, password.value)
    }
    const role = authStore.role
    if (role === 'admin' || role === 'moderator') router.push('/staff')
    else router.push('/dashboard')
  } catch (e: unknown) {
    error.value = e instanceof Error ? e.message : 'Auth failed'
  }
}
</script>
