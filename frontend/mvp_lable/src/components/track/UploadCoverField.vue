<template>
  <div class="flex flex-col gap-2">
    <label class="font-medium text-gray-800">Обложка релиза (.jpg / .jpeg) *</label>
    <p class="text-sm text-gray-500">Требование площадок: строго 3000x3000px, RGB.</p>
    
    <input 
      type="file" 
      accept="image/jpeg" 
      required
      @change="onFileChange"
      class="block w-full text-sm text-gray-500 file:mr-4 file:py-2 file:px-4 file:rounded-md file:border-0 file:text-sm file:font-semibold file:bg-blue-50 file:text-blue-700 hover:file:bg-blue-100 cursor-pointer"
    />
    
    <!-- Предупреждение -->
    <div v-if="warningMessage" class="mt-2 text-sm text-amber-600 bg-amber-50 p-2 rounded border border-amber-200">
      ⚠️ {{ warningMessage }}
    </div>
  </div>
</template>

<script lang="ts">
import { defineComponent } from 'vue'

export default defineComponent({
  name: 'UploadCoverField',
  emits: ['update:file'],
  data() {
    return {
      warningMessage: ''
    }
  },
  methods: {
    onFileChange(e: Event) {
      this.warningMessage = ''
      const target = e.target as HTMLInputElement
      const file = target.files?.[0] || null
      
      this.$emit('update:file', file)

      if (file) {
        this.validateImageSize(file)
      }
    },
    validateImageSize(file: File) {
      const img = new Image()
      const objectUrl = URL.createObjectURL(file)
      
      img.onload = () => {
        if (img.width !== 3000 || img.height !== 3000) {
          this.warningMessage = `Текущий размер: ${img.width}x${img.height}px. Рекомендуется ровно 3000x3000px, иначе площадки могут отклонить релиз.`
        }
        URL.revokeObjectURL(objectUrl) // очищаем память
      }
      
      img.src = objectUrl
    }
  }
})
</script>