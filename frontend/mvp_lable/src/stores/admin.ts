import { defineStore } from 'pinia';

// Тип для пользователя
export interface User {
  id: number;
  name: string;
  email: string;
  status: 'active' | 'blocked';
  registered_at: string;
  // Добавьте другие поля пользователя, если они есть
}

interface AdminState {
  users: User[];
  isLoading: boolean;
  error: string | null;
}

export const useAdminStore = defineStore('admin', {
  // 1. СОСТОЯНИЕ (State)
  state: (): AdminState => ({
    users: [],
    isLoading: false,
    error: null,
  }),

  // 2. ГЕТТЕРЫ (Getters)
  getters: {
    totalUsers(state): number {
      return state.users.length;
    },
    blockedUsersCount(state): number {
      return state.users.filter(u => u.status === 'blocked').length;
    },
  },

  // 3. ДЕЙСТВИЯ (Actions)
  actions: {
    // Загрузка всех пользователей
    async fetchUsers() {
      this.isLoading = true;
      this.error = null;
      try {
        // TODO: Замените на ваш реальный API-запрос
        // const response = await api.get('/admin/users');
        // this.users = response.data;
        
        // --- Mock-данные для симуляции ---
        await new Promise(res => setTimeout(res, 1000));
        this.users = [
            { id: 10, name: 'SynthRider', email: 'synth@label.db', status: 'active', registered_at: '2025-10-15T10:00:00Z' },
            { id: 12, name: 'GridRunner', email: 'grid@label.db', status: 'active', registered_at: '2025-11-20T11:00:00Z' },
            { id: 15, name: 'VoidStalker', email: 'void@label.db', status: 'blocked', registered_at: '2026-01-05T12:00:00Z' },
        ];
        // --- Конец Mock-данных ---

      } catch (e: any) {
        this.error = 'Failed to load users.';
        console.error(e);
      } finally {
        this.isLoading = false;
      }
    },

    // Блокировка пользователя
    async blockUser(userId: number) {
      try {
        // TODO: Замените на ваш реальный API-запрос
        // await api.post(`/admin/users/${userId}/block`);

        // Обновляем статус пользователя в нашем локальном состоянии
        const user = this.users.find(u => u.id === userId);
        if (user) {
          user.status = 'blocked';
        }
      } catch (e) {
        console.error(`Failed to block user ${userId}`, e);
      }
    },

    // Разблокировка пользователя
    async unblockUser(userId: number) {
      try {
        // TODO: Замените на ваш реальный API-запрос
        // await api.post(`/admin/users/${userId}/unblock`);

        const user = this.users.find(u => u.id === userId);
        if (user) {
          user.status = 'active';
        }
      } catch (e) {
        console.error(`Failed to unblock user ${userId}`, e);
      }
    },

     // Удаление пользователя
     async deleteUser(userId: number) {
        try {
            // TODO: Замените на ваш реальный API-запрос
            // await api.delete(`/admin/users/${userId}`);

            this.users = this.users.filter(u => u.id !== userId);
        } catch (e) {
            console.error(`Failed to delete user ${userId}`, e);
        }
     }
  },
});