import { defineStore } from 'pinia'
import type { Permission, SystemRole } from '@/types/permissions'
import { ROLE_DEFAULTS, ALL_ROLES } from '@/types/permissions'

const STORAGE = 'mvp_lable_role_matrix_v2'

export type RoleMatrix = Record<SystemRole, Permission[]>

function seedMatrix(): RoleMatrix {
  return {
    artist: [...ROLE_DEFAULTS.artist],
    moderator: [...ROLE_DEFAULTS.moderator],
    news_editor: [...ROLE_DEFAULTS.news_editor],
    events_editor: [...ROLE_DEFAULTS.events_editor],
    admin: [...ROLE_DEFAULTS.admin],
  }
}

export const usePermissionsStore = defineStore('permissions', {
  state: () => ({
    matrix: seedMatrix() as RoleMatrix,
    matrixDirty: false,
  }),
  getters: {
    roles: () => ALL_ROLES,
  },
  actions: {
    hydrate() {
      try {
        const raw = localStorage.getItem(STORAGE)
        if (raw) this.matrix = { ...seedMatrix(), ...JSON.parse(raw) }
        this.matrixDirty = false
      } catch {
        /* seed */
      }
    },
    persist() {
      localStorage.setItem(STORAGE, JSON.stringify(this.matrix))
    },
    permissionsForRoles(roles: SystemRole[] | string | null): Permission[] {
      const list = Array.isArray(roles)
        ? roles
        : roles
          ? [roles as SystemRole]
          : []
      const set = new Set<Permission>()
      for (const r of list) {
        if (r === 'admin') {
          ;(ROLE_DEFAULTS.admin as Permission[]).forEach((p) => set.add(p))
        }
        const perms = this.matrix[r as SystemRole] || ROLE_DEFAULTS[r as SystemRole] || []
        perms.forEach((p) => set.add(p))
      }
      return [...set]
    },
    permissionsFor(_email: string, role: string | null): Permission[] {
      return this.permissionsForRoles(role)
    },
    setRolePermission(role: SystemRole, key: Permission, on: boolean) {
      if (role === 'admin' && key === 'permissions.manage') return
      const cur = new Set(this.matrix[role] || [])
      if (on) cur.add(key)
      else cur.delete(key)
      this.matrix[role] = [...cur]
      this.matrixDirty = true
    },
    saveMatrix() {
      this.persist()
      this.matrixDirty = false
    },
    discardMatrix() {
      this.hydrate()
      this.matrixDirty = false
    },
  },
})
