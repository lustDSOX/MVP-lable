import { defineStore } from 'pinia'
import type { Permission } from '@/types/permissions'
import { ROLE_DEFAULTS } from '@/types/permissions'

const STORAGE = 'mvp_lable_perm_matrix'

export interface StaffUser {
  id: string
  email: string
  name: string
  role: 'moderator' | 'admin' | 'artist'
  permissions: Permission[]
}

function seed(): StaffUser[] {
  return [
    {
      id: 'u-admin',
      email: 'admin@label.ru',
      name: 'System Overlord',
      role: 'admin',
      permissions: [...ROLE_DEFAULTS.admin],
    },
    {
      id: 'u-mod',
      email: 'moderator@label.ru',
      name: 'Chief Editor',
      role: 'moderator',
      permissions: ['releases.moderate'],
    },
    {
      id: 'u-news',
      email: 'news@label.ru',
      name: 'News Desk',
      role: 'moderator',
      permissions: ['news.manage'],
    },
    {
      id: 'u-events',
      email: 'events@label.ru',
      name: 'Events Desk',
      role: 'moderator',
      permissions: ['events.manage'],
    },
    {
      id: 'u-full',
      email: 'staff@label.ru',
      name: 'Full Staff',
      role: 'moderator',
      permissions: ['releases.moderate', 'news.manage', 'events.manage'],
    },
  ]
}

export const usePermissionsStore = defineStore('permissions', {
  state: () => ({
    staff: seed() as StaffUser[],
    matrixDirty: false,
  }),
  actions: {
    hydrate() {
      try {
        const raw = localStorage.getItem(STORAGE)
        if (raw) this.staff = JSON.parse(raw)
        this.matrixDirty = false
      } catch {
        /* keep seed */
      }
    },
    persist() {
      localStorage.setItem(STORAGE, JSON.stringify(this.staff))
    },
    permissionsFor(email: string, role: string | null): Permission[] {
      const e = (email || '').toLowerCase()
      const row = this.staff.find((s) => s.email.toLowerCase() === e)
      if (row) return [...row.permissions]
      if (role === 'admin') return [...ROLE_DEFAULTS.admin]
      if (role === 'moderator') return [...ROLE_DEFAULTS.moderator]
      return []
    },
    setPermission(userId: string, key: Permission, on: boolean) {
      const u = this.staff.find((s) => s.id === userId)
      if (!u) return
      if (on && !u.permissions.includes(key)) u.permissions.push(key)
      if (!on) u.permissions = u.permissions.filter((p) => p !== key)
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
    addStaff(email: string, name: string, role: 'moderator' | 'admin') {
      this.staff.push({
        id: `u-${Date.now()}`,
        email: email.toLowerCase(),
        name,
        role,
        permissions: role === 'admin' ? [...ROLE_DEFAULTS.admin] : [...ROLE_DEFAULTS.moderator],
      })
      this.matrixDirty = true
    },
  },
})
