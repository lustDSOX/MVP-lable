<template>
  <div class="relative" v-if="authed.isAuthenticated">
    <button
      type="button"
      class="relative min-w-[44px] min-h-[44px] border-2 border-[#444] bg-[#111] px-2 text-[#39FF14] font-mono text-xs"
      aria-label="Уведомления"
      @click="open = !open"
    >
      ✉
      <span
        v-if="unread > 0"
        class="absolute -top-1 -right-1 bg-[#ff0000] text-white text-[9px] font-bold min-w-[16px] h-4 px-1 flex items-center justify-center"
      >{{ unread > 9 ? '9+' : unread }}</span>
    </button>
    <div
      v-if="open"
      class="absolute right-0 top-full mt-2 w-[min(100vw-2rem,22rem)] max-h-[70vh] overflow-y-auto border-2 border-[#39FF14] bg-black z-[80] shadow-[4px_4px_0_#000]"
    >
      <div class="flex justify-between items-center p-2 border-b border-[#333] sticky top-0 bg-black">
        <span class="font-mono text-[10px] uppercase text-[#39FF14]">Уведомления</span>
        <div class="flex gap-2">
          <button type="button" class="font-mono text-[9px] text-gray-500 uppercase" @click="markAll">Все прочит.</button>
          <router-link to="/notifications" class="font-mono text-[9px] text-[#39FF14] uppercase" @click="open = false">Все →</router-link>
        </div>
      </div>
      <button
        v-for="n in list.slice(0, 12)"
        :key="n.id"
        type="button"
        class="block w-full text-left p-3 border-b border-[#222] hover:bg-[#111]"
        :class="{ 'opacity-60': n.read }"
        @click="onClick(n)"
      >
        <p class="font-mono text-[10px] text-[#39FF14] uppercase">{{ n.title }}</p>
        <p class="text-xs text-gray-300 mt-1 line-clamp-4 whitespace-pre-wrap">{{ n.body }}</p>
        <p class="font-mono text-[9px] text-gray-600 mt-1">{{ fmt(n.createdAt) }}</p>
      </button>
      <p v-if="!list.length" class="p-4 font-mono text-xs text-gray-600 text-center">Пусто</p>
      <router-link
        to="/notifications"
        class="block text-center py-3 font-mono text-[10px] uppercase text-[#39FF14] border-t border-[#333]"
        @click="open = false"
      >
        Открыть центр уведомлений
      </router-link>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed, onMounted, ref } from 'vue'
import { useAuthStore } from '@/stores/auth'
import { useNotificationsStore, type AppNotification } from '@/stores/notifications'

const authed = useAuthStore()
const store = useNotificationsStore()
const open = ref(false)
onMounted(() => store.hydrate())
const list = computed(() => (authed.email ? store.forUser(authed.email) : []))
const unread = computed(() => (authed.email ? store.unreadCount(authed.email) : 0))
function markAll() {
  if (authed.email) store.markAllRead(authed.email)
}
function onClick(n: AppNotification) {
  store.markRead(n.id)
}
function fmt(iso: string) {
  try {
    return new Date(iso).toLocaleString()
  } catch {
    return iso
  }
}
</script>
