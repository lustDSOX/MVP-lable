<template>
  <section class="space-y-6">
    <form class="border-2 border-[#333] p-4 space-y-3" @submit.prevent="save">
      <p class="font-mono text-xs text-[#39FF14] uppercase">{{ editingId ? 'Edit' : 'New' }} news · Markdown</p>
      <input v-model="form.title" required placeholder="TITLE" class="field" />
      <input v-model="form.excerpt" placeholder="EXCERPT" class="field" />
      <input v-model="form.date" type="date" class="field" />
      <select v-model="form.status" class="field">
        <option value="draft">draft</option>
        <option value="published">published</option>
      </select>
      <div class="grid md:grid-cols-2 gap-3">
        <div>
          <p class="font-mono text-[10px] text-gray-500 mb-1">MD SOURCE</p>
          <textarea v-model="form.body" rows="12" placeholder="# Title" class="field font-mono text-sm" />
        </div>
        <div>
          <p class="font-mono text-[10px] text-gray-500 mb-1">PREVIEW</p>
          <div class="border-2 border-[#333] bg-black p-4 min-h-[200px] prose-preview" v-html="mdPreview(form.body)" />
        </div>
      </div>
      <div class="flex gap-2 flex-wrap">
        <button type="submit" class="btn-green">Save</button>
        <button v-if="editingId" type="button" class="btn-muted" @click="reset">Cancel</button>
      </div>
    </form>
    <article v-for="n in filtered" :key="n.id" class="border border-[#333] p-4 flex flex-col sm:flex-row sm:items-center gap-3 justify-between">
      <div>
        <p class="font-mono text-sm uppercase text-white">{{ n.title }}</p>
        <p class="font-mono text-[10px] text-gray-500">{{ n.status }} · {{ n.date }}</p>
      </div>
      <div class="flex gap-2">
        <button type="button" class="btn-muted" @click="edit(n)">Edit</button>
        <button type="button" class="btn-red" @click="cms.deleteNews(n.id)">Del</button>
      </div>
    </article>
  </section>
</template>

<script setup lang="ts">
import { computed, reactive, ref, watch } from 'vue'
import { useCmsStore, type NewsItem } from '@/stores/cms'

const props = defineProps<{ tabQuery: string; focusId?: string | null }>()
const cms = useCmsStore()
const editingId = ref<string | null>(null)
const form = reactive({
  title: '',
  excerpt: '',
  body: '',
  date: new Date().toISOString().slice(0, 10),
  status: 'draft' as 'draft' | 'published',
})

watch(
  () => props.focusId,
  (id) => {
    if (!id) return
    const n = cms.news.find((x) => x.id === id)
    if (n) edit(n)
  },
  { immediate: true },
)

const filtered = computed(() => {
  const q = props.tabQuery.trim().toLowerCase()
  if (!q) return cms.news
  return cms.news.filter(
    (n) =>
      n.title.toLowerCase().includes(q) ||
      n.excerpt.toLowerCase().includes(q) ||
      n.body.toLowerCase().includes(q),
  )
})

function mdPreview(src: string): string {
  let s = src || ''
  s = s.replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;')
  s = s.replace(/^### (.*)$/gm, '<h3>$1</h3>')
  s = s.replace(/^## (.*)$/gm, '<h2>$1</h2>')
  s = s.replace(/^# (.*)$/gm, '<h1>$1</h1>')
  s = s.replace(/\*\*(.+?)\*\*/g, '<strong>$1</strong>')
  s = s.replace(/`([^`]+)`/g, '<code>$1</code>')
  s = s.replace(/\[([^\]]+)\]\(([^)]+)\)/g, '<a href="$2" class="text-[#39FF14] underline">$1</a>')
  s = s.replace(/^- (.*)$/gm, '<li>$1</li>')
  s = s.replace(/(<li>.*<\/li>\n?)+/g, (m) => `<ul>${m}</ul>`)
  s = s.replace(/\n\n/g, '</p><p>')
  return `<p>${s}</p>`
}

function reset() {
  editingId.value = null
  form.title = ''
  form.excerpt = ''
  form.body = ''
  form.date = new Date().toISOString().slice(0, 10)
  form.status = 'draft'
}
function edit(n: NewsItem) {
  editingId.value = n.id
  form.title = n.title
  form.excerpt = n.excerpt
  form.body = n.body
  form.date = n.date
  form.status = n.status
}
function save() {
  cms.upsertNews({
    id: editingId.value || undefined,
    title: form.title,
    excerpt: form.excerpt,
    body: form.body,
    date: form.date,
    status: form.status,
  })
  reset()
}
</script>

<style scoped>
.field { display: block; width: 100%; background: #000; border: 2px solid #333; color: #fff; padding: 0.75rem; font-family: 'JetBrains Mono', monospace; font-size: 0.875rem; }
.btn-green { background: #39ff14; color: #000; font-family: 'JetBrains Mono', monospace; font-size: 0.75rem; text-transform: uppercase; padding: 0.5rem 1rem; min-height: 44px; border: 2px solid #000; font-weight: 700; }
.btn-red { background: #ff0000; color: #fff; font-family: 'JetBrains Mono', monospace; font-size: 0.75rem; text-transform: uppercase; padding: 0.5rem 1rem; min-height: 44px; border: 2px solid #000; }
.btn-muted { background: #222; color: #ccc; font-family: 'JetBrains Mono', monospace; font-size: 0.75rem; text-transform: uppercase; padding: 0.5rem 1rem; min-height: 44px; border: 2px solid #444; }
.prose-preview :deep(h1), .prose-preview :deep(h2), .prose-preview :deep(h3) { font-weight: 900; text-transform: uppercase; margin: 0.5em 0; }
.prose-preview :deep(ul) { list-style: disc; padding-left: 1.25rem; }
.prose-preview :deep(code) { background: #111; padding: 0 0.25rem; color: #39ff14; }
</style>
