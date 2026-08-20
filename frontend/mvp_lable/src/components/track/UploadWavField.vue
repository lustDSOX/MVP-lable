<template>
  <div
    class="flex flex-col gap-2 border-2 border-dashed border-[#333] p-4"
    :class="{ 'border-[#39FF14] bg-[#0a1a0a]': over }"
    @dragover.prevent="over = true"
    @dragleave.prevent="over = false"
    @drop.prevent="onDrop"
  >
    <label class="font-mono text-xs uppercase text-gray-400">Аудио (.wav) *</label>
    <p class="font-mono text-[10px] text-gray-500">drag & drop или выбор файла</p>
    <input type="file" accept=".wav,audio/wav,audio/*" class="block w-full text-xs text-gray-400" @change="onChange" />
  </div>
</template>

<script lang="ts">
import { defineComponent } from 'vue'
export default defineComponent({
  name: 'UploadWavField',
  emits: ['update:file'],
  data() {
    return { over: false }
  },
  methods: {
    onChange(e: Event) {
      const target = e.target as HTMLInputElement
      this.$emit('update:file', target.files?.[0] || null)
    },
    onDrop(e: DragEvent) {
      this.over = false
      this.$emit('update:file', e.dataTransfer?.files?.[0] || null)
    },
  },
})
</script>
