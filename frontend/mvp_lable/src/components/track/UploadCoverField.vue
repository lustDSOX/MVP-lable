<template>
  <div
    class="flex flex-col gap-2 border-2 border-dashed border-[#333] p-4"
    :class="{ 'border-[#39FF14] bg-[#0a1a0a]': over }"
    @dragover.prevent="over = true"
    @dragleave.prevent="over = false"
    @drop.prevent="onDrop"
  >
    <label class="font-mono text-xs uppercase text-gray-400">Обложка (.jpg) *</label>
    <p class="font-mono text-[10px] text-gray-500">3000×3000 RGB · drag & drop</p>
    <input type="file" accept="image/jpeg,image/png,image/*" class="block w-full text-xs text-gray-400" @change="onFileChange" />
    <div v-if="warningMessage" class="mt-2 text-xs text-amber-500 font-mono">{{ warningMessage }}</div>
  </div>
</template>

<script lang="ts">
import { defineComponent } from 'vue'
export default defineComponent({
  name: 'UploadCoverField',
  emits: ['update:file'],
  data() {
    return { warningMessage: '', over: false }
  },
  methods: {
    handleFile(file: File | null) {
      this.warningMessage = ''
      this.$emit('update:file', file)
      if (file) this.validateImageSize(file)
    },
    onFileChange(e: Event) {
      const target = e.target as HTMLInputElement
      this.handleFile(target.files?.[0] || null)
    },
    onDrop(e: DragEvent) {
      this.over = false
      this.handleFile(e.dataTransfer?.files?.[0] || null)
    },
    validateImageSize(file: File) {
      const img = new Image()
      const objectUrl = URL.createObjectURL(file)
      img.onload = () => {
        if (img.width !== 3000 || img.height !== 3000) {
          this.warningMessage = `Сейчас ${img.width}×${img.height}. Рекомендуется 3000×3000.`
        }
        URL.revokeObjectURL(objectUrl)
      }
      img.src = objectUrl
    },
  },
})
</script>
