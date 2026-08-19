<template>
  <section class="space-y-6">
    <form class="border-2 border-[#333] p-4 space-y-3" @submit.prevent="save">
      <p class="font-mono text-xs text-[#39FF14] uppercase">{{ editingId ? 'Редактирование' : 'Новая' }} новость · Markdown</p>
      <label class="block"><span class="lbl">Заголовок</span><input v-model="form.title" required class="field" placeholder="GRID_OPENING" /></label>
      <label class="block"><span class="lbl">Краткое описание</span><input v-model="form.excerpt" class="field" placeholder="Лейбл открывает сезон" /></label>
      <div class="grid sm:grid-cols-2 gap-3">
        <label class="block"><span class="lbl">Дата</span><input v-model="form.date" type="date" class="field" /></label>
        <label class="block"><span class="lbl">Статус</span>
          <select v-model="form.status" class="field"><option value="draft">draft (черновик)</option><option value="published">published</option></select>
        </label>
      </div>
      <div>
        <span class="lbl">Текст (Markdown)</span>
        <div class="flex flex-wrap gap-1 mt-1 mb-1">
          <button v-for="b in toolbar" :key="b.tip" type="button" class="tool" :title="b.tip" @click="insert(b.md)">{{ b.label }}</button>
        </div>
        <textarea v-model="form.body" rows="12" class="field font-mono text-sm" placeholder="# Заголовок\n\n**жирный**, [ссылка](url), ![img](url)" />
      </div>
      <div class="border-2 border-[#39FF14]/20 p-4">
        <p class="font-mono text-[10px] text-gray-500 uppercase mb-3">Предпросмотр как на /news</p>
        <div class="y2k-preview p-4 sm:p-6">
          <div class="flex justify-between font-mono text-[10px] text-gray-500 uppercase mb-4"><span>SOURCE SOX</span><span>[{{ form.date }}]</span></div>
          <h2 class="text-2xl sm:text-4xl font-black uppercase italic tracking-tighter mb-4">{{ form.title || 'TITLE' }}</h2>
          <p v-if="form.excerpt" class="text-gray-400 font-mono text-sm mb-4">{{ form.excerpt }}</p>
          <div class="prose-preview text-gray-200" v-html="mdPreview(form.body)" />
        </div>
      </div>
      <div class="flex gap-2 flex-wrap">
        <button type="submit" class="btn-green">Сохранить</button>
        <button v-if="editingId" type="button" class="btn-muted" @click="reset">Отмена</button>
      </div>
    </form>
    <article v-for="n in filtered" :key="n.id" class="border border-[#333] p-4 flex flex-col sm:flex-row sm:items-center gap-3 justify-between">
      <div><p class="font-mono text-sm uppercase text-white">{{ n.title }}</p><p class="font-mono text-[10px] text-gray-500">{{ n.status }} · {{ n.date }}</p></div>
      <div class="flex gap-2"><button type="button" class="btn-muted" @click="edit(n)">Изменить</button><button type="button" class="btn-red" @click="cms.deleteNews(n.id)">Удалить</button></div>
    </article>
  </section>
</template>

<script setup lang="ts">
import { computed, reactive, ref, watch } from 'vue'
import { useCmsStore, type NewsItem } from '@/stores/cms'

const props = defineProps<{ tabQuery: string; focusId?: string | null }>()
const cms = useCmsStore()
const editingId = ref<string | null>(null)
const form = reactive({ title: '', excerpt: '', body: '', date: new Date().toISOString().slice(0, 10), status: 'draft' as 'draft' | 'published' })
const toolbar = [
  { label: 'H1', tip: 'H1', md: '# ' }, { label: 'H2', tip: 'H2', md: '## ' },
  { label: 'B', tip: 'Bold', md: '**текст**' }, { label: 'I', tip: 'Italic', md: '*текст*' },
  { label: 'Link', tip: 'Link', md: '[текст](https://)' }, { label: 'Img', tip: 'Image', md: '![alt](https://picsum.photos/800/400)' },
  { label: 'Code', tip: 'Code', md: '`code`' }, { label: 'List', tip: 'List', md: '- пункт\n' }, { label: 'Quote', tip: 'Quote', md: '> цитата\n' },
]
watch(() => props.focusId, (id) => { if (!id) return; const n = cms.news.find((x) => x.id === id); if (n) edit(n) }, { immediate: true })
const filtered = computed(() => {
  const q = props.tabQuery.trim().toLowerCase()
  if (!q) return cms.news
  return cms.news.filter((n) => n.title.toLowerCase().includes(q) || n.excerpt.toLowerCase().includes(q) || n.body.toLowerCase().includes(q))
})
function insert(md: string) { form.body = (form.body || '') + (form.body && !form.body.endsWith('\n') ? '\n' : '') + md }
function mdPreview(src: string): string {
  let s = src || ''
  s = s.replace(/&/g, '&').replace(/</g, '<').replace(/>/g, '>')
  s = s.replace(/!\[([^\]]*)\]\(([^)]+)\)/g, '<img src="$2" alt="$1" class="max-w-full my-3 border border-[#333]" />')
  s = s.replace(/^### (.*)$/gm, '<h3 class="text-lg font-black uppercase mt-3">$1</h3>')
  s = s.replace(/^## (.*)$/gm, '<h2 class="text-xl font-black uppercase mt-3">$1</h2>')
  s = s.replace(/^# (.*)$/gm, '<h1 class="text-2xl font-black uppercase mt-3">$1</h1>')
  s = s.replace(/^> (.*)$/gm, '<blockquote class="border-l-4 border-[#39FF14] pl-3 text-gray-400 my-2">$1</blockquote>')
  s = s.replace(/\*\*(.+?)\*\*/g, '<strong>$1</strong>').replace(/\*(.+?)\*/g, '<em>$1</em>')
  s = s.replace(/`([^`]+)`/g, '<code class="bg-[#111] text-[#39FF14] px-1">$1</code>')
  s = s.replace(/\[([^\]]+)\]\(([^)]+)\)/g, '<a href="$2" class="text-[#39FF14] underline" target="_blank" rel="noopener">$1</a>')
  s = s.replace(/^- (.*)$/gm, '<li>$1</li>')
  s = s.replace(/(<li>.*<\/li>\n?)+/g, (m) => `<ul class="list-disc pl-5 my-2">${m}</ul>`)
  s = s.replace(/\n\n/g, '</p><p class="my-2">')
  return `<p class="my-2">${s}</p>`
}
function reset() { editingId.value = null; form.title = ''; form.excerpt = ''; form.body = ''; form.date = new Date().toISOString().slice(0, 10); form.status = 'draft' }
function edit(n: NewsItem) { editingId.value = n.id; form.title = n.title; form.excerpt = n.excerpt; form.body = n.body; form.date = n.date; form.status = n.status }
function save() { cms.upsertNews({ id: editingId.value || undefined, title: form.title, excerpt: form.excerpt, body: form.body, date: form.date, status: form.status }); reset() }
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
.prose-preview :deep(h1), .prose-preview :deep(h2), .prose-preview :deep(h3) { font-weight: 900; text-transform: uppercase; margin: 0.5em 0; }
</style>
