<template>
  <Teleport to="body">
    <div v-if="open" class="fixed inset-0 z-[100] flex items-center justify-center bg-black/85 p-3 sm:p-6" @click.self="$emit('cancel')">
      <div class="w-full max-w-3xl max-h-[92vh] flex flex-col border-2 border-[#ff0000] bg-[#0a0a0a] shadow-[8px_8px_0_#000]">
        <div class="p-4 sm:p-5 border-b border-[#333] shrink-0">
          <h3 class="font-mono text-base sm:text-lg uppercase text-[#ff0000]">{{ title }}</h3>
          <p v-if="hint" class="font-mono text-[11px] text-gray-500 mt-1">{{ hint }}</p>
        </div>
        <div class="p-4 sm:p-5 flex-1 overflow-y-auto min-h-0">
          <label class="block h-full">
            <span class="font-mono text-[10px] text-gray-400 uppercase">Текст (уйдёт в уведомление / email)</span>
            <textarea
              v-model="local"
              rows="14"
              class="mt-2 w-full min-h-[280px] sm:min-h-[360px] bg-black border-2 border-[#333] text-white p-4 font-mono text-sm leading-relaxed focus:border-[#ff0000] outline-none resize-y"
              placeholder="Подробно опишите причину или требования…"
            />
          </label>
        </div>
        <div class="p-4 sm:p-5 border-t border-[#333] flex flex-wrap gap-2 justify-end shrink-0">
          <button type="button" class="btn-muted" @click="$emit('cancel')">Отмена</button>
          <button type="button" class="btn-red" :disabled="!local.trim()" @click="$emit('confirm', local.trim())">Отправить</button>
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
.btn-red { background: #ff0000; color: #fff; font-family: 'JetBrains Mono', monospace; font-size: 0.75rem; text-transform: uppercase; padding: 0.65rem 1.25rem; min-height: 48px; border: 2px solid #000; }
.btn-red:disabled { opacity: 0.4; }
.btn-muted { background: #222; color: #ccc; font-family: 'JetBrains Mono', monospace; font-size: 0.75rem; text-transform: uppercase; padding: 0.65rem 1.25rem; min-height: 48px; border: 2px solid #444; }
</style>
