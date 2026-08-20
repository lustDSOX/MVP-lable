<template>
  <section class="border-2 border-[#39FF14] bg-[#050505] p-4 sm:p-6 space-y-4">
    <h2 class="font-mono text-sm uppercase text-[#39FF14]">Admin // Принудительные уведомления</h2>
    <p class="font-mono text-[10px] text-gray-500">Отправка конкретному email или группе ролей. Staff без этой панели шлёт только через approve/reject/правки.</p>

    <label class="block">
      <span class="lbl">Режим</span>
      <select v-model="mode" class="field">
        <option value="user">Конкретный пользователь</option>
        <option value="roles">Группа по ролям</option>
      </select>
    </label>

    <label v-if="mode === 'user'" class="block">
      <span class="lbl">Email</span>
      <input v-model="email" class="field" placeholder="demo@label.ru" list="demo-emails" />
      <datalist id="demo-emails">
        <option v-for="e in allEmails" :key="e" :value="e" />
      </datalist>
    </label>

    <div v-else class="flex flex-wrap gap-3">
      <label v-for="r in roleOptions" :key="r" class="font-mono text-xs flex items-center gap-2">
        <input type="checkbox" :value="r" v-model="roles" class="accent-[#39FF14]" /> {{ r }}
      </label>
    </div>

    <label class="block">
      <span class="lbl">Заголовок</span>
      <input v-model="title" class="field" />
    </label>
    <label class="block">
      <span class="lbl">Текст</span>
      <textarea v-model="body" rows="4" class="field" />
    </label>

    <button type="button" class="btn" @click="send">Отправить</button>
    <p v-if="msg" class="font-mono text-xs text-[#39FF14]">{{ msg }}</p>
  </section>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { useNotificationsStore } from '@/stores/notifications'

const notif = useNotificationsStore()
notif.hydrate()

const mode = ref<'user' | 'roles'>('user')
const email = ref('demo@label.ru')
const roles = ref<string[]>(['artist'])
const title = ref('Сообщение от лейбла')
const body = ref('')
const msg = ref('')

const allEmails = [
  'demo@label.ru',
  'admin@label.ru',
  'moderator@label.ru',
  'manager@label.ru',
  'news@label.ru',
  'events@label.ru',
  'staff@label.ru',
]
const roleOptions = ['artist', 'moderator', 'admin']
const roleEmails: Record<string, string[]> = {
  artist: ['demo@label.ru'],
  moderator: ['moderator@label.ru', 'manager@label.ru', 'news@label.ru', 'events@label.ru', 'staff@label.ru'],
  admin: ['admin@label.ru'],
}

function send() {
  if (!title.value.trim() || !body.value.trim()) {
    msg.value = 'Заполните заголовок и текст'
    return
  }
  if (mode.value === 'user') {
    if (!email.value.includes('@')) {
      msg.value = 'Некорректный email'
      return
    }
    notif.notifyUser(email.value.trim(), title.value.trim(), body.value.trim())
    msg.value = `Отправлено → ${email.value}`
  } else {
    if (!roles.value.length) {
      msg.value = 'Выберите роли'
      return
    }
    const n = notif.notifyRoles(roles.value, title.value.trim(), body.value.trim(), roleEmails)
    msg.value = `Отправлено пользователям: ${n}`
  }
}
</script>

<style scoped>
.lbl { font-family: 'JetBrains Mono', monospace; font-size: 10px; text-transform: uppercase; color: #9ca3af; display: block; margin-bottom: 0.25rem; }
.field { display: block; width: 100%; background: #000; border: 2px solid #333; color: #fff; padding: 0.75rem; font-family: 'JetBrains Mono', monospace; font-size: 0.875rem; }
.btn { background: #39ff14; color: #000; font-family: 'JetBrains Mono', monospace; font-size: 0.75rem; text-transform: uppercase; padding: 0.5rem 1rem; min-height: 44px; border: 2px solid #000; font-weight: 700; }
</style>
