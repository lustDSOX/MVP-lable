<template>
  <!-- Хедер: Жесткий карбоновый фон, толстая кроваво-красная граница снизу -->
  <header class="z-30 bg-[url('https://www.transparenttextures.com/patterns/carbon-fibre.png')] bg-[#050505] font-['Impact','Arial_Black',sans-serif]">
    

    <nav class="max-w-7xl mx-auto px-4 lg:px-6">
      <div class="flex items-stretch justify-between h-20">
        
        <!-- Логотип: Лейбл-стикер с жесткой тенью и глитч-ховером -->
        <div class="flex items-center">
          <router-link to="/" class="group relative flex items-center gap-2 bg-[#ff0000] text-black px-4 py-2 border-2 border-black hover:bg-black hover:text-[#ff0000] hover:border-[#ff0000] transition-none active:shadow-none active:translate-y-1 active:translate-x-1">
            <span class="text-4xl font-black uppercase tracking-tighter scale-y-125 inline-block mt-1">
              .SOX
            </span>
            <!-- Индикатор записи -->
            <div class="hidden sm:flex flex-col ml-2 border-l-2 border-black group-hover:border-[#ff0000] pl-2">
              <span class="text-[10px] font-mono leading-none font-bold">REC</span>
              <span class="text-[10px] font-mono leading-none animate-pulse">● 00:00</span>
            </div>
          </router-link>
        </div>
        
        <!-- Навигация: Микшерный пульт. Пункты вдавлены в панель -->
        <ul class="hidden lg:flex items-stretch border-l-4 border-[#222] ml-8">
          <li class="flex items-stretch">
            <router-link to="/" class="flex items-center px-5 border-r border-[#222] text-gray-500 font-mono text-sm tracking-widest hover:bg-white hover:text-black transition-none shadow-[inset_0_0_15px_rgba(0,0,0,1)] hover:shadow-none group relative">
              <span class="group-hover:font-black group-hover:scale-x-110 inline-block transition-none">ГЛАВНАЯ</span>
              <span class="absolute bottom-0 left-0 w-full h-1 bg-[#39FF14] hidden group-hover:block"></span>
            </router-link>
          </li>
          <li class="flex items-stretch">
            <router-link to="/about" class="flex items-center px-5 border-r border-[#222] text-gray-500 font-mono text-sm tracking-widest hover:bg-white hover:text-black transition-none shadow-[inset_0_0_15px_rgba(0,0,0,1)] hover:shadow-none group relative">
              <span class="group-hover:font-black group-hover:scale-x-110 inline-block transition-none">О_НАС</span>
              <span class="absolute bottom-0 left-0 w-full h-1 bg-[#39FF14] hidden group-hover:block"></span>
            </router-link>
          </li>
          <li class="flex items-stretch">
            <router-link to="/cases" class="flex items-center px-5 border-r border-[#222] text-gray-500 font-mono text-sm tracking-widest hover:bg-white hover:text-black transition-none shadow-[inset_0_0_15px_rgba(0,0,0,1)] hover:shadow-none group relative">
              <span class="group-hover:font-black group-hover:scale-x-110 inline-block transition-none">КЕЙСЫ</span>
              <span class="absolute bottom-0 left-0 w-full h-1 bg-[#39FF14] hidden group-hover:block"></span>
            </router-link>
          </li>
          <li class="flex items-stretch">
            <router-link to="/news" class="flex items-center px-5 border-r border-[#222] text-gray-500 font-mono text-sm tracking-widest hover:bg-white hover:text-black transition-none shadow-[inset_0_0_15px_rgba(0,0,0,1)] hover:shadow-none group relative">
              <span class="group-hover:font-black group-hover:scale-x-110 inline-block transition-none">НОВОСТИ</span>
              <span class="absolute bottom-0 left-0 w-full h-1 bg-[#39FF14] hidden group-hover:block"></span>
            </router-link>
          </li>
          <li class="flex items-stretch">
            <router-link to="/events" class="flex items-center px-5 border-r border-[#222] text-gray-500 font-mono text-sm tracking-widest hover:bg-white hover:text-black transition-none shadow-[inset_0_0_15px_rgba(0,0,0,1)] hover:shadow-none group relative">
              <span class="group-hover:font-black group-hover:scale-x-110 inline-block transition-none">МЕРОПРИЯТИЯ</span>
              <span class="absolute bottom-0 left-0 w-full h-1 bg-[#39FF14] hidden group-hover:block"></span>
            </router-link>
          </li>
          <li class="flex items-stretch">
            <router-link to="/guides" class="flex items-center px-5 border-r-4 border-[#222] text-gray-500 font-mono text-sm tracking-widest hover:bg-white hover:text-black transition-none shadow-[inset_0_0_15px_rgba(0,0,0,1)] hover:shadow-none group relative">
              <span class="group-hover:font-black group-hover:scale-x-110 inline-block transition-none">ДЛЯ_АРТИСТОВ</span>
              <span class="absolute bottom-0 left-0 w-full h-1 bg-[#39FF14] hidden group-hover:block"></span>
            </router-link>
          </li>

         <li v-if="!authed.isAuthenticated" class="flex items-center pl-6">
            <div class="w-40 h-11.5 relative"> 
              <router-link to="/login" class="absolute inset-0 bg-[#39FF14] text-black uppercase text-xl flex items-center justify-center border-2 border-black shadow-[4px_4px_0_#fff] hover:shadow-none hover:translate-x-1 hover:translate-y-1 hover:bg-black hover:text-[#39FF14] hover:border-[#39FF14] transition-none whitespace-nowrap">
                [ ВХОД ]
              </router-link>
            </div>
          </li>

          <li v-else class="flex items-center pl-6">
            <div class="w-45 h-11.5 relative group"> 
              <router-link 
              :to="cabinetPath"
              class="absolute inset-0 bg-[#39FF14] text-black uppercase text-xl flex items-center justify-center border-2 border-black shadow-[4px_4px_0_#fff] hover:shadow-none hover:translate-x-1 hover:translate-y-1 hover:bg-black hover:text-[#39FF14] hover:border-[#39FF14] transition-none whitespace-nowrap">
                [ КАБИНЕТ ]
                <span class="invisible group-hover:visible animate-ping ml-1">_</span>
              </router-link>
            </div>
          </li>
        </ul>
        
        <!-- Мобильный гамбургер: Строгий тумблер -->
        <div class="flex items-center lg:hidden">
          <button class="bg-[#111] border-2 border-[#444] p-2 text-[#39FF14] shadow-[4px_4px_0_#ff0000] hover:bg-[#39FF14] hover:text-black hover:border-black active:shadow-none active:translate-x-1 active:translate-y-1 transition-none">
            <!-- Хардкорные линии вместо мягкого SVG -->
            <div class="w-6 h-0.75 bg-current mb-1"></div>
            <div class="w-6 h-0.75 bg-current mb-1"></div>
            <div class="w-6 h-0.75 bg-current"></div>
          </button>
        </div>
        
      </div>
    </nav>
  </header>
</template>

<script lang="ts">
import { useAuthStore } from '@/stores/auth';
import { defineComponent, computed } from 'vue'

export default defineComponent({
  name: 'Header',
  setup(){
    const authed = useAuthStore()

    const cabinetPath = computed(() => {
      switch (authed.role) {
        case 'admin':
          return '/admin'
        case 'manager':
          return '/moderator'
        case 'artist':
        default:
          return '/dashboard'
      }
    })

    return {
      authed,
      cabinetPath,
    }
  }
})
</script>