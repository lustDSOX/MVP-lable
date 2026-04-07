<template>
  <div class="flex flex-col gap-3">
    <label class="font-medium text-gray-800">Промо / Лайв-фото (JPEG, до 4 шт.)</label>
    <p class="text-sm text-gray-500">Фотографии артиста для питчинга в плейлисты редакторов.</p>
    
    <div class="grid grid-cols-1 sm:grid-cols-2 gap-4">
      <div v-for="index in 4" :key="index" class="flex flex-col gap-1">
        <span class="text-xs text-gray-500 uppercase tracking-wide">Фото {{ index }}</span>
        <input 
          type="file" 
          accept="image/jpeg"
          @change="(e) => onFileChange(e, index - 1)"
          class="block w-full text-xs text-gray-500 file:mr-2 file:py-1 file:px-2 file:rounded file:border-0 file:font-semibold file:bg-gray-100 hover:file:bg-gray-200 cursor-pointer"
        />
      </div>
    </div>
  </div>
</template>

<script lang="ts">
import { defineComponent } from 'vue'

export default defineComponent({
  name: 'UploadLivePhotos',
  emits: ['update:files'],
  data() {
    return {
      // Храним массив из 4 элементов (null если не загружено)
      files: [null, null, null, null] as (File | null)[]
    }
  },
  methods: {
    onFileChange(e: Event, index: number) {
      const target = e.target as HTMLInputElement
      this.files[index] = target.files?.[0] || null
      
      // Отправляем наверх только загруженные файлы (без null)
      const validFiles = this.files.filter((f): f is File => f !== null)
      this.$emit('update:files', validFiles)
    }
  }
})
</script>