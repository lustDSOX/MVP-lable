<template>
  <component
    :is="tag"
    :type="tag === 'button' ? type : undefined"
    :to="to"
    :href="href"
    :disabled="disabled || loading"
    class="acid-btn"
    :class="[
      `acid-btn--${variant}`,
      `acid-btn--${size}`,
      { 'acid-btn--block': block, 'acid-btn--loading': loading },
    ]"
  >
    <span v-if="loading" class="acid-btn__spin" aria-hidden="true" />
    <slot />
  </component>
</template>

<script lang="ts">
import { defineComponent, computed } from 'vue'

export default defineComponent({
  name: 'AcidButton',
  props: {
    variant: {
      type: String as () => 'acid' | 'alert' | 'ghost' | 'solid',
      default: 'acid',
    },
    size: {
      type: String as () => 'sm' | 'md' | 'lg',
      default: 'md',
    },
    block: { type: Boolean, default: false },
    loading: { type: Boolean, default: false },
    disabled: { type: Boolean, default: false },
    type: { type: String as () => 'button' | 'submit' | 'reset', default: 'button' },
    to: { type: [String, Object], default: undefined },
    href: { type: String, default: undefined },
  },
  setup(props) {
    const tag = computed(() => {
      if (props.to) return 'router-link'
      if (props.href) return 'a'
      return 'button'
    })
    return { tag }
  },
})
</script>

<style scoped>
.acid-btn {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  gap: 0.5rem;
  font-family: var(--font-display, Impact, sans-serif);
  font-weight: 900;
  text-transform: uppercase;
  letter-spacing: 0.04em;
  border: 2px solid #000;
  cursor: pointer;
  user-select: none;
  transition: none;
  min-height: 44px;
  line-height: 1;
}
.acid-btn:disabled {
  opacity: 0.35;
  cursor: not-allowed;
}
.acid-btn--block {
  width: 100%;
}
.acid-btn--sm {
  padding: 0.4rem 0.75rem;
  font-size: 0.85rem;
  min-height: 36px;
}
.acid-btn--md {
  padding: 0.65rem 1.1rem;
  font-size: 1rem;
}
.acid-btn--lg {
  padding: 0.85rem 1.4rem;
  font-size: 1.25rem;
  min-height: 52px;
}
.acid-btn--acid {
  background: var(--acid, #39FF14);
  color: #000;
  box-shadow: 4px 4px 0 #fff;
}
.acid-btn--acid:hover:not(:disabled) {
  background: #000;
  color: var(--acid, #39FF14);
  border-color: var(--acid, #39FF14);
  box-shadow: none;
  transform: translate(2px, 2px);
}
.acid-btn--alert {
  background: var(--alert, #ff0000);
  color: #fff;
  box-shadow: 4px 4px 0 #000;
}
.acid-btn--alert:hover:not(:disabled) {
  background: #000;
  color: var(--alert, #ff0000);
  border-color: var(--alert, #ff0000);
  box-shadow: none;
  transform: translate(2px, 2px);
}
.acid-btn--ghost {
  background: transparent;
  color: var(--acid, #39FF14);
  border-color: var(--acid, #39FF14);
  box-shadow: none;
}
.acid-btn--ghost:hover:not(:disabled) {
  background: var(--acid, #39FF14);
  color: #000;
}
.acid-btn--solid {
  background: #fff;
  color: #000;
  box-shadow: 4px 4px 0 var(--alert, #ff0000);
}
.acid-btn--solid:hover:not(:disabled) {
  background: var(--alert, #ff0000);
  color: #fff;
  box-shadow: none;
  transform: translate(2px, 2px);
}
.acid-btn__spin {
  width: 1em;
  height: 1em;
  border: 2px solid currentColor;
  border-right-color: transparent;
  border-radius: 50%;
  animation: acid-spin 0.6s linear infinite;
}
@keyframes acid-spin {
  to {
    transform: rotate(360deg);
  }
}
</style>
