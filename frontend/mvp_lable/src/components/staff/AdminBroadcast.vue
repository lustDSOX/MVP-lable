<template>
  <section class="grid lg:grid-cols-[1fr_280px] gap-4">
    <div class="border-2 border-[#39FF14] bg-[#050505] p-4 sm:p-6 space-y-4">
      <h2 class="font-mono text-sm uppercase text-[#39FF14]">Admin // Рассылка</h2>

      <label class="block">
        <span class="lbl">Название шаблона (для сохранения)</span>
        <input v-model="templateName" class="field" placeholder="Напр. Анонс модерации" />
      </label>

      <div>
        <span class="lbl mb-2 block">Роли (группы)</span>
        <div class="flex flex-wrap gap-3">
          <label
            v-for="r in roleOptions"
            :key="r"
            class="flex items-center gap-3 border-2 border-[#333] px-4 py-3 min-h-[52px] cursor-pointer hover:border-[#39FF14]"
            :class="{ 'border-[#39FF14] bg-[#0a1a0a]': roles.includes(r) }"
          >
            <input type="checkbox" :value="r" v-model="roles" class="w-5 h-5 accent-[#39FF14] shrink-0" />
            <span class="font-mono text-sm uppercase">{{ r }}</span>
          </label>
        </div>
      </div>

      <div>
        <span class="lbl mb-2 block">Пользователи (несколько)</span>
        <input
          v-model="userQuery"
          class="field"
          placeholder="Ник или email…"
          @focus="userMenu = true"
          @input="userMenu = true"
        />
        <ul v-if="userMenu && filteredUsers.length" class="mt-1 border-2 border-[#333] bg-black max-h-40 overflow-y-auto z-10 relative">
          <li v-for="u in filteredUsers" :key="u.email">
            <button
              type="button"
              class="w-full text-left px-3 py-2 font-mono text-xs hover:bg-[#111] hover:text-[#39FF14]"
              @click="addUser(u.email)"
            >
              {{ u.name }} · {{ u.email }}
            </button>
          </li>
        </ul>
        <div class="flex flex-wrap gap-2 mt-2">
          <span
            v-for="e in selectedUsers"
            :key="e"
            class="inline-flex items-center gap-1 border border-[#39FF14] text-[#39FF14] font-mono text-[10px] px-2 py-1"
          >
            {{ e }}
            <button type="button" class="text-[#ff0000]" @click="selectedUsers = selectedUsers.filter((x) => x !== e)">×</button>
          </span>
        </div>
      </div>

      <label class="block">
        <span class="lbl">Заголовок</span>
        <input v-model="title" class="field" />
      </label>
      <label class="block">
        <span class="lbl">Текст</span>
        <textarea v-model="body" rows="6" class="field" />
      </label>

      <div class="flex flex-wrap gap-2">
        <button type="button" class="btn" @click="send">Отправить</button>
        <button type="button" class="btn-muted" @click="saveTemplate">Сохранить шаблон</button>
      </div>
      <p v-if="msg" class="font-mono text-xs text-[#39FF14]">{{ msg }}</p>
    </div>

    <aside class="border-2 border-[#333] bg-[#0a0a0a] p-4 space-y-3">
      <h3 class="font-mono text-xs uppercase text-gray-400">Сохранённые</h3>
      <button
        v-for="t in templates"
        :key="t.id"
        type="button"
        class="w-full text-left border border-[#333] p-3 hover:border-[#39FF14]"
        @click="loadTemplate(t)"
      >
        <p class="font-mono text-xs text-[#39FF14]">{{ t.name }}</p>
        <p class="font-mono text-[9px] text-gray-500 truncate mt-1">{{ t.title }}</p>
      </button>
      <p v-if="!templates.length" class="font-mono text-[10px] text-gray-600">Пока пусто</p>
      <button
        v-if="activeTemplateId"
        type="button"
        class="w-full font-mono text-[10px] text-[#ff0000] border border-[#ff0000] py-2"
        @click="deleteTemplate"
      >
        Удалить выбранный
      </button>
    </aside>
  </section>
</template>

<script setup lang="ts">
import { computed, onMounted, onUnmounted, ref } from 'vue'
import { useNotificationsStore } from '@/stores/notifications'

const TKEY = 'mvp_broadcast_templates_v1'

type Tpl = {
  id: string
  name: string
  title: string
  body: string
  roles: string[]
  users: string[]
}

const notif = useNotificationsStore()
notif.hydrate()

const roles = ref<string[]>([])
const selectedUsers = ref<string[]>([])
const userQuery = ref('')
const userMenu = ref(false)
const title = ref('Сообщение от лейбла')
const body = ref('')
const templateName = ref('')
const templates = ref<Tpl[]>([])
const activeTemplateId = ref<string | null>(null)
const msg = ref('')

const roleOptions = ['artist', 'moderator', 'admin']
const allUsers = [
  { email: 'demo@label.ru', name: 'DJ Neon' },
  { email: 'admin@label.ru', name: 'System Overlord' },
  { email: 'moderator@label.ru', name: 'Chief Editor' },
  { email: 'manager@label.ru', name: 'Manager' },
  { email: 'news@label.ru', name: 'News Desk' },
  { email: 'events@label.ru', name: 'Events Desk' },
  { email: 'staff@label.ru', name: 'Full Staff' },
]
const roleEmails: Record<string, string[]> = {
  artist: ['demo@label.ru'],
  moderator: ['moderator@label.ru', 'manager@label.ru', 'news@label.ru', 'events@label.ru', 'staff@label.ru'],
  admin: ['admin@label.ru'],
}

const filteredUsers = computed(() => {
  const q = userQuery.value.trim().toLowerCase()
  return allUsers.filter(
    (u) =>
      !selectedUsers.value.includes(u.email) &&
      (!q || u.email.toLowerCase().includes(q) || u.name.toLowerCase().includes(q)),
  )
})

function addUser(email: string) {
  if (!selectedUsers.value.includes(email)) selectedUsers.value.push(email)
  userQuery.value = ''
  userMenu.value = false
}

function closeMenu(e: MouseEvent) {
  const t = e.target as HTMLElement
  if (!t.closest?.('.field') && !t.closest?.('ul')) userMenu.value = false
}

onMounted(() => {
  try {
    const raw = localStorage.getItem(TKEY)
    if (raw) templates.value = JSON.parse(raw)
  } catch { /* */ }
  document.addEventListener('click', closeMenu)
})
onUnmounted(() => document.removeEventListener('click', closeMenu))

function persistTemplates() {
  localStorage.setItem(TKEY, JSON.stringify(templates.value))
}

function saveTemplate() {
  const name = templateName.value.trim() || title.value.trim() || 'Без названия'
  const tpl: Tpl = {
    id: activeTemplateId.value || `tpl-${Date.now()}`,
    name,
    title: title.value,
    body: body.value,
    roles: [...roles.value],
    users: [...selectedUsers.value],
  }
  const i = templates.value.findIndex((x) => x.id === tpl.id)
  if (i >= 0) templates.value[i] = tpl
  else templates.value.unshift(tpl)
  activeTemplateId.value = tpl.id
  persistTemplates()
  msg.value = `Шаблон «${name}» сохранён`
}

function loadTemplate(t: Tpl) {
  activeTemplateId.value = t.id
  templateName.value = t.name
  title.value = t.title
  body.value = t.body
  roles.value = [...t.roles]
  selectedUsers.value = [...t.users]
  msg.value = `Загружен «${t.name}»`
}

function deleteTemplate() {
  if (!activeTemplateId.value) return
  templates.value = templates.value.filter((x) => x.id !== activeTemplateId.value)
  activeTemplateId.value = null
  persistTemplates()
  msg.value = 'Шаблон удалён'
}

function send() {
  if (!title.value.trim() || !body.value.trim()) {
    msg.value = 'Заполните заголовок и текст'
    return
  }
  if (!roles.value.length && !selectedUsers.value.length) {
    msg.value = 'Выберите роли и/или пользователей'
    return
  }
  const targets = new Set<string>()
  for (const r of roles.value) {
    for (const e of roleEmails[r] || []) targets.add(e.toLowerCase())
  }
  for (const e of selectedUsers.value) targets.add(e.toLowerCase())
  for (const email of targets) {
    notif.notifyUser(email, title.value.trim(), body.value.trim())
  }
  msg.value = `Отправлено: ${targets.size} получател(ей)`
}
</script>

<style scoped>
.lbl { font-family: 'JetBrains Mono', monospace; font-size: 10px; text-transform: uppercase; color: #9ca3af; display: block; margin-bottom: 0.25rem; }
.field { display: block; width: 100%; background: #000; border: 2px solid #333; color: #fff; padding: 0.75rem; font-family: 'JetBrains Mono', monospace; font-size: 0.875rem; }
.btn { background: #39ff14; color: #000; font-family: 'JetBrains Mono', monospace; font-size: 0.75rem; text-transform: uppercase; padding: 0.5rem 1rem; min-height: 44px; border: 2px solid #000; font-weight: 700; }
.btn-muted { background: #222; color: #ccc; font-family: 'JetBrains Mono', monospace; font-size: 0.75rem; text-transform: uppercase; padding: 0.5rem 1rem; min-height: 44px; border: 2px solid #444; }
</style>
