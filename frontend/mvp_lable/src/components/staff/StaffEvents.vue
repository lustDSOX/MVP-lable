<template>
  <section class="space-y-4">
    <div class="grid lg:grid-cols-[280px_1fr] gap-4 items-start">
      <div class="border-2 border-[#333] max-h-[70vh] overflow-y-auto">
        <button type="button" class="w-full text-left px-3 py-3 font-mono text-xs border-b border-[#222] text-[#39FF14]" @click="startNew">+ Новое событие</button>
        <button v-for="ev in filtered" :key="ev.id" type="button" class="w-full text-left px-3 py-3 border-b border-[#222] hover:bg-[#111]" :class="selectedId === ev.id ? 'bg-[#111] border-l-4 border-l-[#39FF14]' : ''" @click="select(ev)">
          <p class="font-mono text-xs uppercase text-white truncate">{{ ev.title }}</p>
          <p class="font-mono text-[9px] text-gray-500">{{ ev.status }} · {{ ev.date }} · {{ ev.city }}</p>
        </button>
      </div>
      <div ref="formEl" class="border-2 border-[#333] p-4 space-y-3 pb-20 relative">
        <template v-if="selectedId || creating || form.title">
          <p class="font-mono text-xs text-[#39FF14] uppercase">{{ editingId ? 'Редактирование' : 'Новое' }} событие</p>
          <label class="block"><span class="lbl">Название</span><input v-model="form.title" required class="field" placeholder="UNDERGROUND_NIGHT" /></label>
          <div class="grid sm:grid-cols-2 gap-2">
            <label class="block"><span class="lbl">Площадка</span><input v-model="form.venue" class="field" placeholder="Club Void" /></label>
            <label class="block"><span class="lbl">Город</span><input v-model="form.city" class="field" placeholder="Moscow" /></label>
            <label class="block"><span class="lbl">Дата</span><input v-model="form.date" class="field" placeholder="15 AUG" /></label>
            <label class="block"><span class="lbl">Время</span><input v-model="form.time" class="field" placeholder="23:00" /></label>
            <label class="block"><span class="lbl">Цена</span><input v-model="form.price" class="field" placeholder="1500 RUB" /></label>
            <label class="block"><span class="lbl">Вместимость</span><input v-model="form.capacity" class="field" placeholder="400" /></label>
            <label class="block"><span class="lbl">Возраст</span><input v-model="form.ageLimit" class="field" placeholder="18+" /></label>
            <label class="block"><span class="lbl">Ссылка на оплату</span><input v-model="form.ticketUrl" class="field" placeholder="/purchase" /></label>
          </div>
          <label class="block"><span class="lbl">Описание</span><textarea v-model="form.description" rows="3" class="field" placeholder="Live set…" /></label>
          <label class="block"><span class="lbl">Статус</span><select v-model="form.status" class="field"><option value="draft">draft</option><option value="published">published</option></select></label>
          <div class="sticky-actions">
            <button type="button" class="btn-green" @click="save">Сохранить</button>
            <a v-if="form.ticketUrl" :href="form.ticketUrl" class="btn-muted inline-flex items-center" target="_blank" rel="noopener">Открыть оплату</a>
            <button v-if="editingId" type="button" class="btn-red" @click="remove">Удалить</button>
            <button type="button" class="btn-muted" @click="reset">Очистить</button>
          </div>
        </template>
        <p v-else class="font-mono text-sm text-gray-500">Выбери событие слева или создай новое</p>
      </div>
    </div>
  </section>
</template>

<script setup lang="ts">
import { computed, nextTick, reactive, ref, watch } from 'vue'
import { useCmsStore, type EventItem } from '@/stores/cms'

const props = defineProps<{ tabQuery: string; focusId?: string | null }>()
const cms = useCmsStore()
const selectedId = ref<string | null>(null)
const editingId = ref<string | null>(null)
const creating = ref(false)
const formEl = ref<HTMLElement | null>(null)
const form = reactive({
  title: '', venue: '', city: '', date: '15 AUG', time: '23:00', description: '',
  status: 'draft' as 'draft' | 'published', ticketUrl: '/purchase', price: '', capacity: '', ageLimit: '18+',
})

watch(() => props.focusId, (id) => { if (!id) return; const ev = cms.events.find((e) => e.id === id); if (ev) select(ev) }, { immediate: true })

const filtered = computed(() => {
  const q = props.tabQuery.trim().toLowerCase()
  if (!q) return cms.events
  return cms.events.filter((e) => e.title.toLowerCase().includes(q) || e.city.toLowerCase().includes(q) || e.venue.toLowerCase().includes(q) || e.description.toLowerCase().includes(q))
})

function reset() {
  editingId.value = null; selectedId.value = null; creating.value = false
  form.title = ''; form.venue = ''; form.city = ''; form.date = '15 AUG'; form.time = '23:00'
  form.description = ''; form.status = 'draft'; form.ticketUrl = '/purchase'; form.price = ''; form.capacity = ''; form.ageLimit = '18+'
}
function startNew() { reset(); creating.value = true }
async function select(ev: EventItem) {
  selectedId.value = ev.id; editingId.value = ev.id; creating.value = false
  form.title = ev.title; form.venue = ev.venue; form.city = ev.city; form.date = ev.date; form.time = ev.time
  form.description = ev.description; form.status = ev.status
  form.ticketUrl = ev.ticketUrl || '/purchase'; form.price = ev.price || ''; form.capacity = ev.capacity || ''; form.ageLimit = ev.ageLimit || '18+'
  await nextTick()
  formEl.value?.scrollIntoView({ behavior: 'smooth', block: 'start' })
}
function save() {
  cms.upsertEvent({ id: editingId.value || undefined, title: form.title, venue: form.venue, city: form.city, date: form.date, time: form.time, description: form.description, status: form.status, ticketUrl: form.ticketUrl, price: form.price, capacity: form.capacity, ageLimit: form.ageLimit })
  reset()
}
function remove() { if (editingId.value) { cms.deleteEvent(editingId.value); reset() } }
</script>

<style scoped>
.field { display: block; width: 100%; background: #000; border: 2px solid #333; color: #fff; padding: 0.75rem; font-family: 'JetBrains Mono', monospace; font-size: 0.875rem; margin-top: 0.25rem; }
.lbl { font-family: 'JetBrains Mono', monospace; font-size: 10px; text-transform: uppercase; color: #9ca3af; }
.btn-green { background: #39ff14; color: #000; font-family: 'JetBrains Mono', monospace; font-size: 0.75rem; text-transform: uppercase; padding: 0.5rem 1rem; min-height: 44px; border: 2px solid #000; font-weight: 700; }
.btn-red { background: #ff0000; color: #fff; font-family: 'JetBrains Mono', monospace; font-size: 0.75rem; text-transform: uppercase; padding: 0.5rem 1rem; min-height: 44px; border: 2px solid #000; }
.btn-muted { background: #222; color: #ccc; font-family: 'JetBrains Mono', monospace; font-size: 0.75rem; text-transform: uppercase; padding: 0.5rem 1rem; min-height: 44px; border: 2px solid #444; }
.sticky-actions {
  position: sticky;
  bottom: 0;
  z-index: 20;
  display: flex;
  flex-wrap: wrap;
  gap: 0.5rem;
  padding: 0.75rem;
  margin: 0 -1rem -1rem;
  background: rgba(10, 10, 10, 0.95);
  border-top: 2px solid #39ff14;
  backdrop-filter: blur(8px);
}
</style>
