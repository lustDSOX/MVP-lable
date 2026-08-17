<template>
  <span
    class="inline-flex items-center px-2 py-0.5 text-[10px] sm:text-xs font-mono font-bold uppercase tracking-wider border-2"
    :class="toneClass"
  >
    <slot />
  </span>
</template>

<script lang="ts">
import { defineComponent, computed } from 'vue'
export default defineComponent({
  name: 'Tag',
  props: {
    tone: { type: String as () => 'acid' | 'alert' | 'muted' | 'cyan', default: 'acid' },
  },
  setup(props) {
    const toneClass = computed(() => {
      switch (props.tone) {
        case 'alert':
          return 'border-[#ff0000] text-[#ff0000] bg-[#ff0000]/10'
        case 'muted':
          return 'border-[#444] text-[#888] bg-transparent'
        case 'cyan':
          return 'border-[#00ffff] text-[#00ffff] bg-[#00ffff]/10'
        default:
          return 'border-[#39FF14] text-[#39FF14] bg-[#39FF14]/10'
      }
    })
    return { toneClass }
  },
})
</script>
