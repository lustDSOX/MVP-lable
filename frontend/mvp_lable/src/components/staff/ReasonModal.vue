<template>
  <Teleport to="body">
    <div v-if="open" class="fixed inset-0 z-[100] flex items-center justify-center bg-black/80 p-4" @click.self="$emit('cancel')">
      <div class="w-full max-w-md border-2 border-[#ff0000] bg-[#0a0a0a] p-5 space-y-4">
        <h3 class="font-mono text-sm uppercase text-[#ff0000]">{{ title }}</h3>
        <p v-if="hint" class="font-mono text-[10px] text-gray-500">{{ hint }}</p>
        <label class="block">
          <span class="font-mono text-[10px] text-gray-400 uppercase">Причина (уйдёт на email)</span>
          <textarea v-model="local" rows="4" class="mt-1 w-full bg-black border-2 border-[#333] text-white p-3 font-mono text-sm" placeholder="Укажите причину…" />
        </label>
        <div class="flex gap-2 justify-end">
          <button type="button" class="btn-muted" @click="$emit('cancel')">Отмена</button>
          <button type="button" class="btn-red" :disabled="!local.trim()" @click="$emit('confirm', local.trim())">Отправить отказ</button>
        </div>
      </div>
    </div>
  </Teleport>
</template>

<script setup lang="ts">
import { ref, watch } from 'vue'
const props = defineProps<{ open: boolean; title?: string; hint?: string; initial?: string }>()
defineEmits<{ confirm: [reason: string]; cancel: [] }>()
const local = ref('')
watch(() => props.open, (v) => { if (v) local.value = props.initial || '' })
</script>

<style scoped>
.btn-red { background: #ff0000; color: #fff; font-family: 'JetBrains Mono', monospace; font-size: 0.75rem; text-transform: uppercase; padding: 0.5rem 1rem; min-height: 44px; border: 2px solid #000; }
.btn-red:disabled { opacity: 0.4; }
.btn-muted { background: #222; color: #ccc; font-family: 'JetBrains Mono', monospace; font-size: 0.75rem; text-transform: uppercase; padding: 0.5rem 1rem; min-height: 44px; border: 2px solid #444; }
</style>
