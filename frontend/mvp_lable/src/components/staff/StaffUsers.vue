<template>
  <section class="space-y-8">
    <div>
      <p class="font-mono text-xs text-[#39FF14] uppercase mb-3">Заявки на регистрацию ({{ admin.requests.length }})</p>
      <article v-for="req in filteredReqs" :key="req.id" class="border border-[#333] p-4 mb-2 flex flex-col sm:flex-row sm:items-center justify-between gap-3">
        <div>
          <p class="font-mono text-sm text-white">{{ req.artistName }} · {{ req.name }}</p>
          <p class="font-mono text-[10px] text-gray-500">{{ req.email }} · {{ req.createdAt }}</p>
          <p v-if="req.note" class="font-mono text-[10px] text-gray-400">{{ req.note }}</p>
        </div>
        <div class="flex gap-2">
          <button type="button" class="btn-green" @click="admin.approveRequest(req.id)">Approve</button>
          <button type="button" class="btn-red" @click="admin.rejectRequest(req.id)">Reject</button>
        </div>
      </article>
      <p v-if="!filteredReqs.length" class="font-mono text-gray-600 text-sm">Нет заявок</p>
    </div>
    <div>
      <p class="font-mono text-xs text-[#39FF14] uppercase mb-3">Аккаунты</p>
      <form class="border border-[#333] p-4 space-y-2 mb-4" @submit.prevent="save">
        <p class="font-mono text-[10px] text-gray-500">{{ editingId ? 'Edit' : 'New' }} account</p>
        <input v-model="form.name" required placeholder="NAME" class="field" />
        <input v-model="form.email" required type="email" placeholder="EMAIL" class="field" />
        <select v-model="form.role" class="field">
          <option value="artist">artist</option>
          <option value="moderator">moderator</option>
          <option value="admin">admin</option>
        </select>
        <select v-model="form.status" class="field">
          <option value="active">active</option>
          <option value="blocked">blocked</option>
        </select>
        <div class="flex gap-2">
          <button type="submit" class="btn-green">Save</button>
          <button v-if="editingId" type="button" class="btn-muted" @click="reset">Cancel</button>
        </div>
      </form>
      <article v-for="u in filteredUsers" :key="u.id" class="border border-[#333] p-4 mb-2 flex flex-col sm:flex-row sm:items-center justify-between gap-3">
        <div>
          <p class="font-mono text-sm text-white">{{ u.name }}</p>
          <p class="font-mono text-[10px] text-gray-500">{{ u.email }} · {{ u.role }} · {{ u.status }}</p>
        </div>
        <div class="flex flex-wrap gap-2">
          <button type="button" class="btn-muted" @click="edit(u)">Edit</button>
          <button v-if="u.status !== 'blocked'" type="button" class="btn-red" @click="admin.blockUser(u.id)">Block</button>
          <button v-else type="button" class="btn-green" @click="admin.unblockUser(u.id)">Unblock</button>
          <button type="button" class="btn-muted" @click="admin.deleteUser(u.id)">Del</button>
        </div>
      </article>
    </div>
  </section>
</template>

<script setup lang="ts">
import { computed, reactive, ref } from 'vue'
import { useAdminStore, type Account } from '@/stores/admin'

const props = defineProps<{ tabQuery: string }>()
const admin = useAdminStore()
const editingId = ref<string | null>(null)
const form = reactive({
  name: '',
  email: '',
  role: 'artist' as Account['role'],
  status: 'active' as Account['status'],
})

const filteredUsers = computed(() => {
  const q = props.tabQuery.trim().toLowerCase()
  if (!q) return admin.users
  return admin.users.filter(
    (u) => u.email.toLowerCase().includes(q) || u.name.toLowerCase().includes(q) || u.role.includes(q),
  )
})
const filteredReqs = computed(() => {
  const q = props.tabQuery.trim().toLowerCase()
  if (!q) return admin.requests
  return admin.requests.filter(
    (r) =>
      r.email.toLowerCase().includes(q) ||
      r.name.toLowerCase().includes(q) ||
      r.artistName.toLowerCase().includes(q),
  )
})

function reset() {
  editingId.value = null
  form.name = ''
  form.email = ''
  form.role = 'artist'
  form.status = 'active'
}
function edit(u: Account) {
  editingId.value = u.id
  form.name = u.name
  form.email = u.email
  form.role = u.role
  form.status = u.status
}
function save() {
  admin.upsertUser({
    id: editingId.value || undefined,
    name: form.name,
    email: form.email,
    role: form.role,
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
</style>
