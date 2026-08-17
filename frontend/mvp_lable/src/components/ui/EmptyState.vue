<template>
  <div
    class="w-full border-4 border-dashed border-[#333] bg-black/60 px-6 py-12 sm:py-16 text-center"
    role="status"
  >
    <p class="font-mono text-[10px] sm:text-xs tracking-[0.35em] text-[#39FF14] mb-3 uppercase">
      {{ code }}
    </p>
    <h2 class="text-2xl sm:text-4xl font-black uppercase italic text-white mb-3 leading-none">
      {{ title }}
    </h2>
    <p v-if="description" class="font-mono text-sm text-gray-500 max-w-md mx-auto mb-6 leading-relaxed">
      {{ description }}
    </p>
    <slot />
  </div>
</template>

<script lang="ts">
import { defineComponent } from 'vue'
export default defineComponent({
  name: 'EmptyState',
  props: {
    code: { type: String, default: 'NULL_SET' },
    title: { type: String, default: 'Nothing here' },
    description: { type: String, default: '' },
  },
})
</script>
