<template>
  <div class="genre-picker relative">
    <div class="flex flex-wrap gap-2 mb-2 min-h-[28px]">
      <span
        v-for="g in selected"
        :key="g"
        class="inline-flex items-center gap-1 border border-[#39FF14] text-[#39FF14] font-mono text-[10px] uppercase px-2 py-1"
      >
        {{ g }}
        <button type="button" class="text-[#ff0000] leading-none" aria-label="remove" @click="remove(g)">×</button>
      </span>
      <span v-if="!selected.length" class="font-mono text-[10px] text-gray-600">Не выбрано</span>
    </div>
    <input
      v-model="q"
      type="search"
      class="field"
      placeholder="Поиск жанра…"
      @focus="open = true"
      @keydown.enter.prevent="addFirst"
    />
    <ul v-if="open && filtered.length" class="absolute left-0 right-0 z-20 mt-1 max-h-48 overflow-y-auto border-2 border-[#333] bg-black text-gray-200">
      <li v-for="g in filtered" :key="g">
        <button type="button" class="w-full text-left px-3 py-2 font-mono text-xs uppercase text-gray-200 hover:bg-[#111] hover:text-[#39FF14]" @click="add(g)">
          {{ g }}
        </button>
      </li>
    </ul>
  </div>
</template>

<script setup lang="ts">
import { computed, onMounted, onUnmounted, ref } from 'vue'
import { GENRE_OPTIONS } from '@/constants/genres'

const props = withDefaults(defineProps<{ modelValue?: string[] }>(), { modelValue: () => [] })
const emit = defineEmits<{ 'update:modelValue': [string[]] }>()

const q = ref('')
const open = ref(false)
const selected = computed(() => props.modelValue || [])

const filtered = computed(() => {
  const query = q.value.trim().toLowerCase()
  return GENRE_OPTIONS.filter(
    (g) => !selected.value.includes(g) && (!query || g.toLowerCase().includes(query)),
  )
})

function add(g: string) {
  if (selected.value.includes(g)) return
  emit('update:modelValue', [...selected.value, g])
  q.value = ''
  open.value = false
}
function remove(g: string) {
  emit('update:modelValue', selected.value.filter((x) => x !== g))
}
function addFirst() {
  if (filtered.value[0]) add(filtered.value[0])
}
function onDoc(e: MouseEvent) {
  const t = e.target as HTMLElement
  if (!t.closest?.('.genre-picker')) open.value = false
}
onMounted(() => document.addEventListener('click', onDoc))
onUnmounted(() => document.removeEventListener('click', onDoc))
</script>

<style scoped>
.field { display: block; width: 100%; background: #000; border: 2px solid #333; color: #fff; padding: 0.75rem; font-family: 'JetBrains Mono', monospace; font-size: 0.875rem; }
</style>
