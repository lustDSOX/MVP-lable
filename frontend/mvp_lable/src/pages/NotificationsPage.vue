<template>
  <div class="min-h-screen pt-24 px-4 pb-16 text-white font-['Inter',sans-serif]">
    <div class="max-w-2xl mx-auto">
      <div class="flex flex-wrap items-center justify-between gap-3 mb-6 border-b-4 border-[#39FF14] pb-4">
        <h1 class="text-2xl sm:text-3xl font-black uppercase italic">Уведомления</h1>
        <button type="button" class="font-mono text-xs uppercase border border-[#333] px-3 py-2 min-h-[44px]" @click="markAll">Прочитать все</button>
      </div>
      <p v-if="!auth.email" class="font-mono text-sm text-gray-500">Войдите, чтобы видеть уведомления.</p>
      <div v-else class="space-y-3">
        <article
          v-for="n in list"
          :key="n.id"
          class="border-2 p-4 cursor-pointer"
          :class="n.read ? 'border-[#222] opacity-70' : 'border-[#39FF14] bg-[#050a05]'"
          @click="store.markRead(n.id)"
        >
          <div class="flex flex-wrap justify-between gap-2">
            <p class="font-mono text-xs uppercase text-[#39FF14]">{{ n.title }}</p>
            <span class="font-mono text-[9px] text-gray-600">{{ n.type }}</span>
          </div>
          <p class="text-sm text-gray-200 mt-2 whitespace-pre-wrap">{{ n.body }}</p>
          <p class="font-mono text-[9px] text-gray-600 mt-2">{{ fmt(n.createdAt) }}</p>
        </article>
        <p v-if="!list.length" class="font-mono text-sm text-gray-600 text-center py-12">Нет уведомлений</p>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed, onMounted } from 'vue'
import { useAuthStore } from '@/stores/auth'
import { useNotificationsStore } from '@/stores/notifications'

const auth = useAuthStore()
const store = useNotificationsStore()
onMounted(() => store.hydrate())
const list = computed(() => (auth.email ? store.forUser(auth.email) : []))
function markAll() {
  if (auth.email) store.markAllRead(auth.email)
}
function fmt(iso: string) {
  try {
    return new Date(iso).toLocaleString()
  } catch {
    return iso
  }
}
</script>
