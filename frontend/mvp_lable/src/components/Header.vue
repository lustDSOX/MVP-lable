<template>
  <header class="z-30 bg-[url('https://www.transparenttextures.com/patterns/carbon-fibre.png')] bg-[#050505] font-['Impact','Arial_Black',sans-serif] relative">
    <nav class="max-w-7xl mx-auto px-3 sm:px-4 lg:px-6" aria-label="Main">
      <div class="flex items-stretch justify-between h-14 sm:h-16 md:h-20">
        <div class="flex items-center">
          <router-link to="/" class="group relative flex items-center gap-1 sm:gap-2 bg-[#ff0000] text-black px-2 sm:px-3 md:px-4 py-1.5 sm:py-2 border-2 border-black hover:bg-black hover:text-[#ff0000] hover:border-[#ff0000] transition-none active:shadow-none active:translate-y-1 active:translate-x-1">
            <span class="text-2xl sm:text-3xl md:text-4xl font-black uppercase tracking-tighter scale-y-125 inline-block mt-0.5 sm:mt-1">.SOX</span>
            <div class="hidden sm:flex flex-col ml-1 sm:ml-2 border-l-2 border-black group-hover:border-[#ff0000] pl-1.5 sm:pl-2">
              <span class="text-[8px] sm:text-[10px] font-mono leading-none font-bold">REC</span>
              <span class="text-[8px] sm:text-[10px] font-mono leading-none animate-pulse">● 00:00</span>
            </div>
          </router-link>
        </div>
        <ul class="hidden lg:flex items-stretch border-l-4 border-[#222] ml-8">
          <li class="flex items-stretch" v-for="link in navLinks" :key="link.to">
            <router-link :to="link.to" custom v-slot="{ href, navigate, isActive, isExactActive }">
              <a
                :href="href"
                @click="navigate"
                class="flex items-center px-5 border-r border-[#222] text-gray-500 font-mono text-sm tracking-widest hover:bg-white hover:text-black transition-none shadow-[inset_0_0_15px_rgba(0,0,0,1)] hover:shadow-none group relative"
                :class="isNavActive(link.to, isActive, isExactActive) ? '!text-black !bg-[#39FF14] !shadow-none' : ''"
              >
                <span class="group-hover:font-black group-hover:scale-x-110 inline-block transition-none">{{ link.label }}</span>
                <span class="absolute bottom-0 left-0 w-full h-1 bg-[#39FF14]" :class="isNavActive(link.to, isActive, isExactActive) ? 'opacity-100' : 'opacity-0 group-hover:opacity-100'"></span>
              </a>
            </router-link>
          </li>
          <li v-if="!authed.isAuthenticated" class="flex items-center pl-6">
            <div class="w-40 h-11.5 relative">
              <router-link to="/login" class="absolute inset-0 bg-[#39FF14] text-black uppercase text-xl flex items-center justify-center border-2 border-black shadow-[4px_4px_0_#fff] hover:shadow-none hover:translate-x-1 hover:translate-y-1 hover:bg-black hover:text-[#39FF14] hover:border-[#39FF14] transition-none whitespace-nowrap">[ ВХОД ]</router-link>
            </div>
          </li>
          <li v-else class="flex items-center pl-6 gap-2">
            <NotificationBell />
            <router-link :to="cabinetPath" class="bg-[#39FF14] text-black uppercase text-sm px-4 py-2 border-2 border-black font-black hover:bg-black hover:text-[#39FF14] hover:border-[#39FF14]">{{ cabinetLabel }}</router-link>
            <button type="button" class="bg-black text-[#ff0000] uppercase text-sm px-3 py-2 border-2 border-[#ff0000] font-black hover:bg-[#ff0000] hover:text-black min-h-[44px]" @click="logout">[ ВЫХОД ]</button>
          </li>
        </ul>
        <div class="flex items-center gap-2 lg:hidden">
          <NotificationBell v-if="authed.isAuthenticated" />
          <button type="button" @click="menuOpen = !menuOpen" class="bg-[#111] border-2 border-[#444] p-2.5 text-[#39FF14] shadow-[3px_3px_0_#ff0000] hover:bg-[#39FF14] hover:text-black min-w-[44px] min-h-[44px]" :aria-expanded="menuOpen" aria-controls="mobile-nav" aria-label="Toggle menu">
            <div class="w-5 h-0.5 bg-current mb-1"></div>
            <div class="w-5 h-0.5 bg-current mb-1"></div>
            <div class="w-5 h-0.5 bg-current"></div>
          </button>
        </div>
      </div>
    </nav>
    <div v-show="menuOpen" id="mobile-nav" class="lg:hidden absolute left-0 right-0 top-full z-50 bg-[#0a0a0a] border-b-4 border-[#39FF14] shadow-[0_12px_0_#111]">
      <ul class="flex flex-col">
        <li v-for="link in navLinks" :key="link.to">
          <router-link :to="link.to" custom v-slot="{ href, navigate, isActive, isExactActive }">
            <a :href="href" @click="(e) => { navigate(e); menuOpen = false }" class="block px-4 py-3.5 min-h-[48px] border-b border-[#222] text-gray-400 font-mono text-sm tracking-widest hover:bg-white hover:text-black" :class="isNavActive(link.to, isActive, isExactActive) ? '!bg-[#39FF14] !text-black font-black' : ''">{{ link.label }}</a>
          </router-link>
        </li>
        <li class="p-4">
          <router-link v-if="!authed.isAuthenticated" to="/login" @click="menuOpen = false" class="block w-full bg-[#39FF14] text-black uppercase text-lg text-center py-3 border-2 border-black font-black min-h-[48px]">[ ВХОД ]</router-link>
          <template v-else>
            <router-link :to="cabinetPath" @click="menuOpen = false" class="block w-full bg-[#39FF14] text-black uppercase text-lg text-center py-3 border-2 border-black font-black min-h-[48px]">{{ cabinetLabel }}</router-link>
            <button type="button" class="mt-2 block w-full bg-black text-[#ff0000] uppercase text-lg text-center py-3 border-2 border-[#ff0000] font-black min-h-[48px]" @click="logout">[ ВЫХОД ]</button>
          </template>
        </li>
      </ul>
    </div>
  </header>
</template>

<script lang="ts">
import { useAuthStore } from '@/stores/auth'
import NotificationBell from '@/components/ui/NotificationBell.vue'
import { defineComponent, computed, ref, watch } from 'vue'
import { useRoute, useRouter } from 'vue-router'

export default defineComponent({
  name: 'Header',
  components: { NotificationBell },
  setup() {
    const authed = useAuthStore()
    const menuOpen = ref(false)
    const route = useRoute()
    const router = useRouter()

    watch(() => route.fullPath, () => { menuOpen.value = false })

    const navLinks = [
      { to: '/', label: 'ГЛАВНАЯ' },
      { to: '/about', label: 'О_НАС' },
      { to: '/cases', label: 'КЕЙСЫ' },
      { to: '/news', label: 'НОВОСТИ' },
      { to: '/events', label: 'МЕРОПРИЯТИЯ' },
      { to: '/guides', label: 'ДЛЯ_АРТИСТОВ' },
    ]

    const isNavActive = (to: string, isActive: boolean, isExactActive: boolean) =>
      to === '/' ? isExactActive : isActive

    const cabinetPath = computed(() => {
      const role = authed.role
      if (role === 'admin' || role === 'moderator') return '/staff'
      return '/dashboard'
    })
    const cabinetLabel = computed(() => {
      const role = authed.role
      if (role === 'admin') return '[ ADMIN ]'
      if (role === 'moderator') return '[ STAFF ]'
      return '[ КАБИНЕТ ]'
    })

    function logout() {
      authed.logout()
      menuOpen.value = false
      router.push('/')
    }

    return { authed, menuOpen, navLinks, cabinetPath, cabinetLabel, isNavActive, logout }
  },
})
</script>
