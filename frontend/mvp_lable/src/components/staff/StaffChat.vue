<template>
  <section class="border-2 border-[#333] bg-[#0a0a0a] flex flex-col" style="min-height: 420px">
    <div class="border-b border-[#333] p-3 font-mono text-xs text-[#39FF14] uppercase">Internal_Staff_Chat</div>
    <div ref="box" class="flex-1 overflow-y-auto p-3 space-y-3 max-h-[50vh]">
      <article v-for="m in chat.messages" :key="m.id" class="border border-[#222] p-3">
        <div class="flex justify-between gap-2 font-mono text-[10px] text-gray-500">
          <span class="text-[#39FF14]">{{ m.fromName }}</span>
          <span>{{ fmt(m.at) }}</span>
        </div>
        <p class="text-sm text-gray-200 mt-1 whitespace-pre-wrap">{{ m.body }}</p>
      </article>
    </div>
    <form class="border-t border-[#333] p-3 flex gap-2" @submit.prevent="send">
      <input v-model="text" class="flex-1 bg-black border-2 border-[#333] px-3 py-2 font-mono text-sm" placeholder="Сообщение staff…" />
      <button type="submit" class="bg-[#39FF14] text-black font-mono text-xs uppercase px-4 min-h-[44px] border-2 border-black font-bold">Send</button>
    </form>
  </section>
</template>

<script setup lang="ts">
import { nextTick, onMounted, ref, watch } from 'vue'
import { useAuthStore } from '@/stores/auth'
import { useStaffChatStore } from '@/stores/staffChat'

const chat = useStaffChatStore()
const auth = useAuthStore()
const text = ref('')
const box = ref<HTMLElement | null>(null)

onMounted(() => {
  chat.hydrate()
  scroll()
})
watch(() => chat.messages.length, () => scroll())

async function scroll() {
  await nextTick()
  if (box.value) box.value.scrollTop = box.value.scrollHeight
}

function send() {
  chat.send(auth.email || 'staff', auth.artistName || 'Staff', text.value)
  text.value = ''
}
function fmt(iso: string) {
  try {
    return new Date(iso).toLocaleString()
  } catch {
    return iso
  }
}
</script>
