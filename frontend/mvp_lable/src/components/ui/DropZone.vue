<template>
  <div
    class="drop-zone border-2 border-dashed border-[#333] p-4 text-center transition-colors"
    :class="{ 'border-[#39FF14] bg-[#0a1a0a]': over }"
    @dragover.prevent="over = true"
    @dragleave.prevent="over = false"
    @drop.prevent="onDrop"
  >
    <p class="font-mono text-[10px] text-gray-500 uppercase mb-2">{{ label }}</p>
    <slot />
    <label class="btn-muted cursor-pointer inline-flex items-center mt-2">
      {{ buttonLabel }}
      <input type="file" class="hidden" :accept="accept" @change="onFile" />
    </label>
  </div>
</template>

<script setup lang="ts">
import { ref } from 'vue'
withDefaults(defineProps<{ label?: string; buttonLabel?: string; accept?: string }>(), {
  label: 'Перетащите файл сюда',
  buttonLabel: 'Или выберите файл',
  accept: '*/*',
})
const emit = defineEmits<{ file: [File] }>()
const over = ref(false)
function onDrop(e: DragEvent) {
  over.value = false
  const f = e.dataTransfer?.files?.[0]
  if (f) emit('file', f)
}
function onFile(e: Event) {
  const f = (e.target as HTMLInputElement).files?.[0]
  if (f) emit('file', f)
}
</script>

<style scoped>
.btn-muted { background: #222; color: #ccc; font-family: 'JetBrains Mono', monospace; font-size: 0.75rem; text-transform: uppercase; padding: 0.5rem 1rem; min-height: 44px; border: 2px solid #444; }
</style>
