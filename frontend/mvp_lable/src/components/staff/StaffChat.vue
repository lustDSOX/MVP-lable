<template>
  <section class="border-2 border-[#333] bg-[#0a0a0a] grid md:grid-cols-[260px_1fr] min-h-[520px]">
    <aside class="border-b md:border-b-0 md:border-r border-[#333] flex flex-col max-h-[45vh] md:max-h-[75vh]">
      <div class="p-3 border-b border-[#333] space-y-2">
        <p class="font-mono text-[10px] text-[#39FF14] uppercase">Диалоги</p>
        <input v-model="search" type="search" class="w-full bg-black border border-[#333] px-2 py-2 font-mono text-xs" placeholder="Найти пользователя…" />
        <button type="button" class="w-full font-mono text-[10px] uppercase border border-[#39FF14] text-[#39FF14] py-2 min-h-[40px]" @click="showNew = !showNew">+ Новый чат</button>
        <div v-if="showNew" class="border border-[#333] max-h-36 overflow-y-auto">
          <button v-for="u in newCandidates" :key="u.email" type="button" class="w-full text-left px-2 py-2 font-mono text-[10px] hover:bg-[#111] hover:text-[#39FF14]" @click="startChat(u.email)">
            {{ u.name }} · {{ u.email }}
          </button>
        </div>
      </div>
      <div class="overflow-y-auto flex-1">
        <button v-for="p in visiblePeers" :key="p.email" type="button" class="w-full text-left px-3 py-3 border-b border-[#222] hover:bg-[#111]" :class="{ 'bg-[#111] border-l-2 border-l-[#39FF14]': peer === p.email }" @click="peer = p.email">
          <p class="font-mono text-xs text-white truncate">{{ p.name }}</p>
          <p class="font-mono text-[9px] text-gray-500 truncate">{{ p.email }}</p>
          <p v-if="preview(p.email)" class="font-mono text-[9px] text-gray-600 mt-1 truncate">{{ preview(p.email) }}</p>
        </button>
      </div>
    </aside>
    <div class="flex flex-col min-h-[360px] max-h-[75vh]">
      <div class="p-3 border-b border-[#333] font-mono text-xs">
        <span v-if="peer" class="text-[#39FF14]">{{ peerName }}</span>
        <span v-else class="text-gray-600">Выберите собеседника</span>
      </div>
      <div ref="box" class="flex-1 overflow-y-auto p-3 space-y-2">
        <template v-if="peer">
          <div v-for="m in thread" :key="m.id" class="max-w-[90%] p-3 border font-mono text-xs" :class="m.fromEmail.toLowerCase() === me ? 'ml-auto border-[#39FF14] bg-[#0a1a0a]' : 'border-[#333] bg-[#111]'">
            <p class="text-[9px] text-gray-500 mb-1">{{ fmt(m.at) }}</p>
            <p class="text-gray-200 whitespace-pre-wrap break-words">{{ m.body }}</p>
          </div>
          <p v-if="!thread.length" class="text-gray-600 font-mono text-xs text-center py-8">Нет сообщений</p>
        </template>
      </div>
      <form v-if="peer" class="border-t border-[#333] p-3 space-y-2" @submit.prevent="send">
        <textarea v-model="text" rows="4" class="w-full bg-black border-2 border-[#333] px-3 py-2 font-mono text-sm resize-y min-h-[96px]" placeholder="Сообщение (несколько строк)…" @keydown.ctrl.enter.prevent="send" />
        <div class="flex justify-between items-center">
          <span class="font-mono text-[9px] text-gray-600">Ctrl+Enter</span>
          <button type="submit" class="bg-[#39FF14] text-black font-mono text-xs uppercase px-4 min-h-[44px] border-2 border-black font-bold">Send</button>
        </div>
      </form>
    </div>
  </section>
</template>

<script setup lang="ts">
import { computed, nextTick, onMounted, ref, watch } from 'vue'
import { useAuthStore } from '@/stores/auth'
import { useStaffChatStore, ALL_CHAT_USERS } from '@/stores/staffChat'

const chat = useStaffChatStore()
const auth = useAuthStore()
const peer = ref('')
const text = ref('')
const search = ref('')
const showNew = ref(false)
const box = ref<HTMLElement | null>(null)

const me = computed(() => (auth.email || '').toLowerCase())
const peers = computed(() => chat.peersFor(auth.email || ''))
const visiblePeers = computed(() => {
  const q = search.value.trim().toLowerCase()
  return peers.value.filter((p) => !q || p.email.toLowerCase().includes(q) || p.name.toLowerCase().includes(q))
})
const newCandidates = computed(() =>
  ALL_CHAT_USERS.filter(
    (u) => u.email.toLowerCase() !== me.value && !peers.value.some((p) => p.email.toLowerCase() === u.email.toLowerCase()),
  ),
)
const peerName = computed(() => ALL_CHAT_USERS.find((p) => p.email === peer.value)?.name || peer.value)
const thread = computed(() => (peer.value ? chat.thread(auth.email || '', peer.value) : []))

onMounted(() => {
  chat.hydrate()
  if (peers.value[0]) peer.value = peers.value[0].email
})
watch(() => thread.value.length, () => scroll())

async function scroll() {
  await nextTick()
  if (box.value) box.value.scrollTop = box.value.scrollHeight
}
function preview(email: string) {
  return chat.thread(auth.email || '', email).slice(-1)[0]?.body || ''
}
function startChat(email: string) {
  chat.ensurePeer(email)
  peer.value = email
  showNew.value = false
}
function send() {
  if (!peer.value || !text.value.trim()) return
  chat.send(auth.email || 'staff', peer.value, text.value)
  text.value = ''
  scroll()
}
function fmt(iso: string) {
  try { return new Date(iso).toLocaleString() } catch { return iso }
}
</script>
