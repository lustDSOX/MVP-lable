<template>
  <div class="flex flex-col gap-2">
    <label class="font-medium text-gray-800">Пресс-релиз / Описание трека</label>
    <textarea 
      :value="modelValue"
      @input="onInput"
      rows="4"
      placeholder="Расскажите о треке: история создания, настроение, кому понравится..."
      class="w-full px-3 py-2 bg-white text-gray-900 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 resize-y"
    ></textarea>
  </div>
</template>

<script lang="ts">
import { defineComponent } from 'vue'

export default defineComponent({
  name: 'PressReleaseTextarea',
  props: {
    modelValue: { type: String, default: '' }
  },
  emits: ['update:modelValue'],
  methods: {
    onInput(e: Event) {
      const target = e.target as HTMLTextAreaElement
      this.$emit('update:modelValue', target.value)
    }
  }
})
</script>