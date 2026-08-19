<template>
  <section class="space-y-4">
    <div class="flex gap-2 border border-[#333] p-1">
      <button type="button" class="flex-1 min-h-[44px] font-mono text-xs uppercase" :class="sub === 'requests' ? 'bg-[#39FF14] text-black' : 'text-gray-400'" @click="sub = 'requests'">Заявки ({{ admin.requests.length }})</button>
      <button type="button" class="flex-1 min-h-[44px] font-mono text-xs uppercase" :class="sub === 'accounts' ? 'bg-[#39FF14] text-black' : 'text-gray-400'" @click="sub = 'accounts'">Аккаунты ({{ admin.users.length }})</button>
    </div>
    <div v-if="sub === 'requests'" class="space-y-3">
      <article v-for="req in filteredReqs" :key="req.id" class="border border-[#333] p-4 flex flex-col gap-3">
        <div>
          <p class="font-mono text-sm text-white">{{ req.artistName }} · {{ req.name }}</p>
          <p class="font-mono text-[10px] text-gray-500">{{ req.email }} · {{ req.createdAt }}</p>
          <p v-if="req.note" class="font-mono text-[10px] text-gray-400 mt-1">{{ req.note }}</p>
        </div>
        <div class="flex flex-wrap gap-2">
          <button type="button" class="btn-green" @click="admin.approveRequest(req.id, ['artist'])">Одобрить (artist)</button>
          <button type="button" class="btn-red" @click="openReject(req.id)">Отказать</button>
        </div>
      </article>
      <p v-if="!filteredReqs.length" class="font-mono text-gray-600 text-sm">Нет заявок</p>
    </div>
    <div v-else class="space-y-4">
      <form class="border border-[#333] p-4 space-y-3" @submit.prevent="save">
        <p class="font-mono text-[10px] text-[#39FF14] uppercase">{{ editingId ? 'Редактировать' : 'Новый' }} аккаунт</p>
        <label class="block"><span class="lbl">Имя / ник</span><input v-model="form.name" required class="field" placeholder="DJ Neon" /></label>
        <label class="block"><span class="lbl">Email</span><input v-model="form.email" required type="email" class="field" placeholder="user@mail.ru" /></label>
        <fieldset>
          <legend class="lbl mb-2">Роли (можно несколько)</legend>
          <div class="flex flex-wrap gap-3">
            <label v-for="r in ALL_ROLES" :key="r.key" class="flex items-center gap-2 font-mono text-xs text-gray-300">
              <input type="checkbox" class="w-4 h-4 accent-[#39FF14]" :checked="form.roles.includes(r.key)" @change="toggleRole(r.key, ($event.target as HTMLInputElement).checked)" />
              {{ r.label }}
            </label>
          </div>
        </fieldset>
        <label class="block"><span class="lbl">Статус</span><select v-model="form.status" class="field"><option value="active">active</option><option value="blocked">blocked</option></select></label>
        <div class="flex gap-2"><button type="submit" class="btn-green">Сохранить</button><button v-if="editingId" type="button" class="btn-muted" @click="reset">Отмена</button></div>
      </form>
      <article v-for="u in filteredUsers" :key="u.id" class="border border-[#333] p-4 flex flex-col sm:flex-row sm:items-center justify-between gap-3">
        <div>
          <p class="font-mono text-sm text-white">{{ u.name }}</p>
          <p class="font-mono text-[10px] text-gray-500">{{ u.email }} · {{ u.status }}</p>
          <p class="font-mono text-[10px] text-[#39FF14] mt-1">{{ u.roles.join(', ') }}</p>
        </div>
        <div class="flex flex-wrap gap-2">
          <button type="button" class="btn-muted" @click="edit(u)">Изменить</button>
          <button v-if="u.status !== 'blocked'" type="button" class="btn-red" @click="admin.blockUser(u.id)">Блок</button>
          <button v-else type="button" class="btn-green" @click="admin.unblockUser(u.id)">Разблок</button>
          <button type="button" class="btn-muted" @click="admin.deleteUser(u.id)">Удалить</button>
        </div>
      </article>
    </div>
    <ReasonModal :open="rejectOpen" title="Отказ в регистрации" hint="Текст будет отправлен на email заявителя (mock)." @cancel="rejectOpen = false" @confirm="confirmReject" />
  </section>
</template>

<script setup lang="ts">
import { computed, reactive, ref } from 'vue'
import { useAdminStore, type Account } from '@/stores/admin'
import { ALL_ROLES, type SystemRole } from '@/types/permissions'
import ReasonModal from './ReasonModal.vue'

const props = defineProps<{ tabQuery: string }>()
const admin = useAdminStore()
const sub = ref<'requests' | 'accounts'>('requests')
const editingId = ref<string | null>(null)
const rejectOpen = ref(false)
const rejectId = ref<string | null>(null)
const form = reactive({ name: '', email: '', roles: ['artist'] as SystemRole[], status: 'active' as Account['status'] })

const filteredUsers = computed(() => {
  const q = props.tabQuery.trim().toLowerCase()
  if (!q) return admin.users
  return admin.users.filter((u) => u.email.toLowerCase().includes(q) || u.name.toLowerCase().includes(q) || u.roles.some((r) => r.includes(q)))
})
const filteredReqs = computed(() => {
  const q = props.tabQuery.trim().toLowerCase()
  if (!q) return admin.requests
  return admin.requests.filter((r) => r.email.toLowerCase().includes(q) || r.name.toLowerCase().includes(q) || r.artistName.toLowerCase().includes(q))
})

function toggleRole(key: SystemRole, on: boolean) {
  if (on && !form.roles.includes(key)) form.roles.push(key)
  if (!on) form.roles = form.roles.filter((r) => r !== key)
  if (!form.roles.length) form.roles = ['artist']
}
function reset() { editingId.value = null; form.name = ''; form.email = ''; form.roles = ['artist']; form.status = 'active' }
function edit(u: Account) { editingId.value = u.id; form.name = u.name; form.email = u.email; form.roles = [...u.roles]; form.status = u.status }
function save() { admin.upsertUser({ id: editingId.value || undefined, name: form.name, email: form.email, roles: [...form.roles], status: form.status }); reset() }
function openReject(id: string) { rejectId.value = id; rejectOpen.value = true }
function confirmReject(reason: string) { if (rejectId.value) admin.rejectRequest(rejectId.value, reason); rejectOpen.value = false; rejectId.value = null }
</script>

<style scoped>
.field { display: block; width: 100%; background: #000; border: 2px solid #333; color: #fff; padding: 0.75rem; font-family: 'JetBrains Mono', monospace; font-size: 0.875rem; margin-top: 0.25rem; }
.lbl { font-family: 'JetBrains Mono', monospace; font-size: 10px; text-transform: uppercase; color: #9ca3af; }
.btn-green { background: #39ff14; color: #000; font-family: 'JetBrains Mono', monospace; font-size: 0.75rem; text-transform: uppercase; padding: 0.5rem 1rem; min-height: 44px; border: 2px solid #000; font-weight: 700; }
.btn-red { background: #ff0000; color: #fff; font-family: 'JetBrains Mono', monospace; font-size: 0.75rem; text-transform: uppercase; padding: 0.5rem 1rem; min-height: 44px; border: 2px solid #000; }
.btn-muted { background: #222; color: #ccc; font-family: 'JetBrains Mono', monospace; font-size: 0.75rem; text-transform: uppercase; padding: 0.5rem 1rem; min-height: 44px; border: 2px solid #444; }
</style>
