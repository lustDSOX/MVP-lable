<template>
  <div class="flex flex-col gap-2">
    <label class="font-medium text-gray-800">Аудиофайл трека (только .wav) *</label>
    <input 
      type="file" 
      accept=".wav, audio/wav" 
      required
      @change="onChange"
      class="block w-full text-sm text-gray-500 file:mr-4 file:py-2 file:px-4 file:rounded-md file:border-0 file:text-sm file:font-semibold file:bg-blue-50 file:text-blue-700 hover:file:bg-blue-100 cursor-pointer"
    />
  </div>
</template>

<script lang="ts">
import { defineComponent } from 'vue'

export default defineComponent({
  name: 'UploadWavField',
  emits: ['update:file'],
  methods: {
    onChange(e: Event) {
      const target = e.target as HTMLInputElement
      const file = target.files?.[0] || null
      this.$emit('update:file', file)
    }
  }
})
</script>