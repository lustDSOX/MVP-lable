<template>
  <section class="space-y-4 overflow-x-auto">
    <div class="flex flex-wrap gap-2 items-center justify-between">
      <div>
        <p class="font-mono text-xs text-gray-400 uppercase">Матрица ролей</p>
        <p class="font-mono text-[10px] text-gray-600 mt-1">Роль → доступы к разделам</p>
      </div>
      <div class="flex gap-2">
        <button type="button" class="btn-muted" :disabled="!perm.matrixDirty" @click="perm.discardMatrix()">Сбросить</button>
        <button type="button" class="btn-green" :disabled="!perm.matrixDirty" @click="perm.saveMatrix()">Сохранить матрицу</button>
      </div>
    </div>
    <p v-if="perm.matrixDirty" class="font-mono text-[10px] text-[#ff0000]">Есть несохранённые изменения</p>
    <table class="w-full text-left border border-[#333] min-w-[640px]">
      <thead>
        <tr class="border-b border-[#333] font-mono text-[10px] text-gray-500 uppercase">
          <th class="p-3">Роль</th>
          <th v-for="p in ALL_PERMISSIONS" :key="p.key" class="p-2 text-center">{{ p.label }}</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="r in ALL_ROLES" :key="r.key" class="border-b border-[#222]">
          <td class="p-3">
            <p class="font-mono text-xs text-white uppercase">{{ r.label }}</p>
            <p class="font-mono text-[9px] text-gray-500">{{ r.key }}</p>
          </td>
          <td v-for="p in ALL_PERMISSIONS" :key="p.key" class="p-2 text-center">
            <input type="checkbox" class="w-5 h-5 accent-[#39FF14]" :checked="(perm.matrix[r.key] || []).includes(p.key)" :disabled="r.key === 'admin' && p.key === 'permissions.manage'" @change="perm.setRolePermission(r.key, p.key, ($event.target as HTMLInputElement).checked)" />
          </td>
        </tr>
      </tbody>
    </table>
  </section>
</template>

<script setup lang="ts">
import { usePermissionsStore } from '@/stores/permissions'
import { ALL_PERMISSIONS, ALL_ROLES } from '@/types/permissions'
defineProps<{ tabQuery: string }>()
const perm = usePermissionsStore()
</script>

<style scoped>
.btn-green { background: #39ff14; color: #000; font-family: 'JetBrains Mono', monospace; font-size: 0.75rem; text-transform: uppercase; padding: 0.5rem 1rem; min-height: 44px; border: 2px solid #000; font-weight: 700; }
.btn-muted { background: #222; color: #ccc; font-family: 'JetBrains Mono', monospace; font-size: 0.75rem; text-transform: uppercase; padding: 0.5rem 1rem; min-height: 44px; border: 2px solid #444; }
.btn-green:disabled, .btn-muted:disabled { opacity: 0.4; cursor: not-allowed; }
</style>
