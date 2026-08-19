<template>
  <section class="space-y-4 overflow-x-auto">
    <div class="flex flex-wrap gap-2 items-center justify-between">
      <p class="font-mono text-xs text-gray-400 uppercase">Матрица доступа</p>
      <div class="flex gap-2">
        <button type="button" class="btn-muted" :disabled="!perm.matrixDirty" @click="perm.discardMatrix()">Сбросить</button>
        <button type="button" class="btn-green" :disabled="!perm.matrixDirty" @click="perm.saveMatrix()">Сохранить матрицу</button>
      </div>
    </div>
    <p v-if="perm.matrixDirty" class="font-mono text-[10px] text-[#ff0000]">Есть несохранённые изменения</p>
    <table class="w-full text-left border border-[#333] min-w-[640px]">
      <thead>
        <tr class="border-b border-[#333] font-mono text-[10px] text-gray-500 uppercase">
          <th class="p-3">User</th>
          <th v-for="p in ALL_PERMISSIONS" :key="p.key" class="p-2 text-center">{{ p.label.split(' ')[0] }}</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="u in filtered" :key="u.id" class="border-b border-[#222]">
          <td class="p-3">
            <p class="font-mono text-xs text-white">{{ u.email }}</p>
            <p class="font-mono text-[9px] text-gray-500">{{ u.role }} · {{ u.name }}</p>
          </td>
          <td v-for="p in ALL_PERMISSIONS" :key="p.key" class="p-2 text-center">
            <input
              type="checkbox"
              class="w-5 h-5 accent-[#39FF14]"
              :checked="u.permissions.includes(p.key)"
              @change="perm.setPermission(u.id, p.key, ($event.target as HTMLInputElement).checked)"
            />
          </td>
        </tr>
      </tbody>
    </table>
  </section>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import { usePermissionsStore } from '@/stores/permissions'
import { ALL_PERMISSIONS } from '@/types/permissions'

const props = defineProps<{ tabQuery: string }>()
const perm = usePermissionsStore()
const filtered = computed(() => {
  const q = props.tabQuery.trim().toLowerCase()
  if (!q) return perm.staff
  return perm.staff.filter(
    (u) => u.email.toLowerCase().includes(q) || u.name.toLowerCase().includes(q) || u.role.includes(q),
  )
})
</script>

<style scoped>
.btn-green { background: #39ff14; color: #000; font-family: 'JetBrains Mono', monospace; font-size: 0.75rem; text-transform: uppercase; padding: 0.5rem 1rem; min-height: 44px; border: 2px solid #000; font-weight: 700; }
.btn-muted { background: #222; color: #ccc; font-family: 'JetBrains Mono', monospace; font-size: 0.75rem; text-transform: uppercase; padding: 0.5rem 1rem; min-height: 44px; border: 2px solid #444; }
.btn-green:disabled, .btn-muted:disabled { opacity: 0.4; cursor: not-allowed; }
</style>
