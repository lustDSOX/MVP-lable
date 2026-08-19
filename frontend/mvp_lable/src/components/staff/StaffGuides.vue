<template>
  <section class="space-y-6">
    <form ref="formEl" class="border-2 border-[#333] p-4 space-y-3 relative pb-28" @submit.prevent="save">
      <p class="font-mono text-xs text-[#39FF14] uppercase">{{ editingId ? 'Редактирование' : 'Новый' }} гайд · Markdown</p>
      <div v-if="editingId || form.title || form.body" class="form-actions-fixed">
        <button type="submit" class="btn-green">Сохранить</button>
        <button v-if="editingId" type="button" class="btn-muted" @click="reset">Отмена</button>
      </div>
      <label class="block"><span class="lbl">Заголовок</span><input v-model="form.title" required class="field" placeholder="RELEASE_PIPELINE" /></label>
      <label class="block"><span class="lbl">Краткое описание</span><input v-model="form.excerpt" class="field" placeholder="Как сдать релиз" /></label>
      <div class="grid sm:grid-cols-2 gap-3">
        <label class="block"><span class="lbl">Категория</span><input v-model="form.category" class="field" placeholder="releases" /></label>
        <label class="block"><span class="lbl">Статус</span>
          <select v-model="form.status" class="field"><option value="draft">draft</option><option value="published">published</option></select>
        </label>
      </div>
      <div>
        <span class="lbl">Текст (Markdown)</span>
        <div class="flex flex-wrap gap-1 mt-1 mb-1">
          <button v-for="b in toolbar" :key="b.tip" type="button" class="tool" :title="b.tip" @click="insert(b.md)">{{ b.label }}</button>
        </div>
        <textarea v-model="form.body" rows="12" class="field font-mono text-sm" placeholder="# Заголовок" />
      </div>
      <div class="border-2 border-[#39FF14]/20 p-4">
        <p class="font-mono text-[10px] text-gray-500 uppercase mb-3">Предпросмотр</p>
        <div class="y2k-preview p-4">
          <h2 class="text-2xl font-black uppercase italic mb-2">{{ form.title || 'TITLE' }}</h2>
          <div class="prose-preview text-gray-200" v-html="mdToHtml(form.body)" />
        </div>
      </div>
    </form>
    <article
      v-for="n in filtered"
      :key="n.id"
      class="border border-[#333] p-4 flex flex-col sm:flex-row sm:items-center gap-3 justify-between cursor-pointer hover:border-[#39FF14]"
      :class="editingId === n.id ? 'border-[#39FF14]' : ''"
      @click="edit(n)"
    >
      <div>
        <p class="font-mono text-sm uppercase text-white">{{ n.title }}</p>
        <p class="font-mono text-[10px] text-gray-500">{{ n.status }} · {{ n.category }}</p>
      </div>
      <div class="flex gap-2" @click.stop>
        <button type="button" class="btn-muted" @click="edit(n)">Изменить</button>
        <button type="button" class="btn-red" @click="cms.deleteGuide(n.id)">Удалить</button>
      </div>
    </article>
  </section>
</template>

<script setup lang="ts">
import { computed, nextTick, reactive, ref, watch } from 'vue'
import { useCmsStore, type GuideItem } from '@/stores/cms'
import { mdToHtml } from '@/utils/md'

const props = defineProps<{ tabQuery: string; focusId?: string | null }>()
const cms = useCmsStore()
const editingId = ref<string | null>(null)
const formEl = ref<HTMLElement | null>(null)
const form = reactive({
  title: '', excerpt: '', body: '', category: 'general',
  status: 'draft' as 'draft' | 'published',
})
const toolbar = [
  { label: 'H1', tip: 'H1', md: '# ' }, { label: 'H2', tip: 'H2', md: '## ' },
  { label: 'B', tip: 'Bold', md: '**текст**' }, { label: 'Link', tip: 'Link', md: '[текст](https://)' },
  { label: 'Img', tip: 'Image', md: '![alt](https://picsum.photos/800/400)' },
]
watch(() => props.focusId, (id) => { if (!id) return; const n = cms.guides.find((x) => x.id === id); if (n) edit(n) }, { immediate: true })
const filtered = computed(() => {
  const q = props.tabQuery.trim().toLowerCase()
  if (!q) return cms.guides
  return cms.guides.filter((n) => n.title.toLowerCase().includes(q) || n.excerpt.toLowerCase().includes(q) || n.body.toLowerCase().includes(q) || (n.category || '').toLowerCase().includes(q))
})
function insert(md: string) { form.body = (form.body || '') + (form.body && !form.body.endsWith('\n') ? '\n' : '') + md }
function reset() {
  editingId.value = null; form.title = ''; form.excerpt = ''; form.body = ''; form.category = 'general'; form.status = 'draft'
}
async function edit(n: GuideItem) {
  editingId.value = n.id
  form.title = n.title; form.excerpt = n.excerpt; form.body = n.body; form.category = n.category || 'general'; form.status = n.status
  await nextTick()
  formEl.value?.scrollIntoView({ behavior: 'smooth', block: 'start' })
}
function save() {
  cms.upsertGuide({ id: editingId.value || undefined, title: form.title, excerpt: form.excerpt, body: form.body, category: form.category, status: form.status })
  reset()
}
</script>

<style scoped>
.field { display: block; width: 100%; background: #000; border: 2px solid #333; color: #fff; padding: 0.75rem; font-family: 'JetBrains Mono', monospace; font-size: 0.875rem; margin-top: 0.25rem; }
.lbl { font-family: 'JetBrains Mono', monospace; font-size: 10px; text-transform: uppercase; color: #9ca3af; }
.tool { font-family: 'JetBrains Mono', monospace; font-size: 10px; padding: 0.35rem 0.5rem; border: 1px solid #333; color: #aaa; background: #111; min-height: 32px; }
.tool:hover { border-color: #39ff14; color: #39ff14; }
.btn-green { background: #39ff14; color: #000; font-family: 'JetBrains Mono', monospace; font-size: 0.75rem; text-transform: uppercase; padding: 0.5rem 1rem; min-height: 44px; border: 2px solid #000; font-weight: 700; }
.btn-red { background: #ff0000; color: #fff; font-family: 'JetBrains Mono', monospace; font-size: 0.75rem; text-transform: uppercase; padding: 0.5rem 1rem; min-height: 44px; border: 2px solid #000; }
.btn-muted { background: #222; color: #ccc; font-family: 'JetBrains Mono', monospace; font-size: 0.75rem; text-transform: uppercase; padding: 0.5rem 1rem; min-height: 44px; border: 2px solid #444; }
.y2k-preview { background: linear-gradient(135deg, #1a1a1a, #0d0d0d); border: 1px solid #333; }
.form-actions-fixed {
  position: fixed; left: 0; right: 0; bottom: 0; z-index: 60;
  display: flex; flex-wrap: wrap; gap: 0.5rem; justify-content: center;
  padding: 0.75rem 1rem calc(0.75rem + env(safe-area-inset-bottom));
  background: rgba(0, 0, 0, 0.96); border-top: 2px solid #39ff14;
  box-shadow: 0 -4px 20px rgba(0,0,0,0.6);
}
</style>
