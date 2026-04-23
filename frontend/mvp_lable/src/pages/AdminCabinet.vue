<!-- AdminCabinet.vue -->
<template>
  <div class="min-h-screen pt-24 px-4 pb-12 font-['Inter',sans-serif] text-white relative">
    <div class="max-w-7xl mx-auto flex flex-col gap-12 relative z-10">

      <!-- СЕКЦИЯ 1: КОМАНДНЫЙ ЦЕНТР -->
      <section class="command-center-grid">
        <div class="welcome-block">
          <h1 class="font-planet h1-metal-textured" :data-text="authStore.artistName || 'ADMIN'">
            {{ authStore.artistName || 'ADMIN' }}
          </h1>
          <span class="welcome-subtitle">Administrator_Panel</span>
        </div>

        <div class="search-wrapper">
          <input
            type="text"
            v-model="searchQuery"
            placeholder="Search users by name or email..."
            class="search-input"
          />
        </div>

        <button @click="isRegisterModalOpen = true" class="upload-button group">
          <span class="relative z-10 text-2xl">Register New Artist</span>
          <div class="absolute inset-0 crt-noise opacity-30"></div>
        </button>
      </section>

      <!-- СЕКЦИЯ 2: ПАНЕЛЬ ДАННЫХ -->
      <section class="data-panel-container">
        <div class="data-panel-content">
          <div class="stat-item">
            <span class="label">Total Users</span>
            <span class="value">{{ users.length }}</span>
          </div>
          <div class="stat-item">
            <span class="label">Monthly Active</span>
            <span class="value">0</span> <!-- TODO: Implement logic -->
          </div>
          <div class="stat-item">
            <span class="label">Blocked Users</span>
            <span class="value">{{ users.filter(u => u.status === 'blocked').length }}</span>
          </div>
        </div>
      </section>

      <!-- СЕКЦИЯ 3: ТАБЛИЦА ПОЛЬЗОВАТЕЛЕЙ -->
      <section class="bg-black border border-[#333]">
        <div class="overflow-x-auto">
          <table class="w-full text-left min-w-[800px]">
            <thead class="table-header">
              <tr>
                <th class="table-th w-2/5">Artist / Email</th>
                <th class="table-th text-center">Registration Date</th>
                <th class="table-th text-center">Status</th>
                <th class="table-th text-center">Actions</th>
              </tr>
            </thead>
            <tbody>
              <tr v-if="isLoading">
                <td colspan="4" class="p-8 text-center text-[#ff0000] font-mono animate-pulse">LOADING USER DATA...</td>
              </tr>
              <tr v-else-if="filteredUsers.length === 0">
                <td colspan="4" class="p-8 text-center text-gray-600 font-mono">NO USERS FOUND.</td>
              </tr>
              <tr v-for="user in filteredUsers" :key="user.id" class="table-row">
                <td class="p-4">
                    <h3 class="track-title">{{ user.name }}</h3>
                    <span class="text-sm text-gray-400 font-mono">{{ user.email }}</span>
                </td>
                <td class="p-4 text-center font-mono">
                  {{ new Date(user.registered_at).toLocaleDateString() }}
                </td>
                <td class="p-4 text-center">
                  <span v-if="user.status === 'active'" class="status-badge status-online">ACTIVE</span>
                  <span v-else-if="user.status === 'blocked'" class="status-badge status-error">BLOCKED</span>
                </td>
                <td class="p-4">
                  <div class="flex items-center justify-center gap-2">
                     <button @click="editUser(user.id)" class="action-button" title="Edit User Data">
                        <svg xmlns="http://www.w3.org/2000/svg" class="w-5 h-5" viewBox="0 0 20 20" fill="currentColor"><path d="M17.414 2.586a2 2 0 00-2.828 0L7 10.172V13h2.828l7.586-7.586a2 2 0 000-2.828z" /><path fill-rule="evenodd" d="M2 6a2 2 0 012-2h4a1 1 0 010 2H4v10h10v-4a1 1 0 112 0v4a2 2 0 01-2 2H4a2 2 0 01-2-2V6z" clip-rule="evenodd" /></svg>
                     </button>
                     <button v-if="user.status === 'active'" @click="blockUser(user.id)" class="action-button" title="Block User">
                        <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" viewBox="0 0 20 20" fill="currentColor"><path fill-rule="evenodd" d="M13.477 14.89A6 6 0 015.11 6.524l8.367 8.367zm1.414-1.414L6.524 5.11A6 6 0 0114.89 13.477zM18 10a8 8 0 11-16 0 8 8 0 0116 0z" clip-rule="evenodd" /></svg>
                     </button>
                      <button v-else @click="unblockUser(user.id)" class="action-button" title="Unblock User">
                        <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" viewBox="0 0 20 20" fill="currentColor"><path fill-rule="evenodd" d="M10 18a8 8 0 100-16 8 8 0 000 16zm3.707-9.293a1 1 0 00-1.414-1.414L9 10.586 7.707 9.293a1 1 0 00-1.414 1.414l2 2a1 1 0 001.414 0l4-4z" clip-rule="evenodd" /></svg>
                     </button>
                     <button @click="deleteUser(user.id)" class="action-button delete-button" title="Delete User">
                        <svg xmlns="http://www.w3.org/2000/svg" class="h-5 w-5" viewBox="0 0 20 20" fill="currentColor"><path fill-rule="evenodd" d="M9 2a1 1 0 00-.894.553L7.382 4H4a1 1 0 000 2v10a2 2 0 002 2h8a2 2 0 002-2V6a1 1 0 100-2h-3.382l-.724-1.447A1 1 0 0011 2H9zM7 8a1 1 0 012 0v6a1 1 0 11-2 0V8zm5-1a1 1 0 00-1 1v6a1 1 0 102 0V8a1 1 0 00-1-1z" clip-rule="evenodd" /></svg>
                     </button>
                  </div>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </section>
    </div>
    <!-- TODO: Модальное окно для регистрации, редактирования и подтверждения удаления -->
  </div>
</template>

<style scoped>
/* Все стили из ArtistCabinet.vue копируются сюда */
/* ... (скопируйте все содержимое тега <style> из вашего файла) ... */

/* Дополнительные стили */
.action-button.delete-button:hover {
    background-color: #ff0000;
    color: white;
}
</style>

<script lang="ts">
import { defineComponent } from 'vue';
import { useAuthStore } from '@/stores/auth';
// Рекомендуется создать такой стор для логики администрирования
import { useAdminStore, type User } from '@/stores/admin';

export default defineComponent({
  name: 'AdminCabinet',

  setup() {
    return {
      authStore: useAuthStore(),
      adminStore: useAdminStore(),
    }
  },

  data() {
    return {
      searchQuery: '',
      isRegisterModalOpen: false,
    };
  },

  computed: {
    users(): User[] {
      return this.adminStore.users; // Геттер из стора
    },
    isLoading(): boolean {
      return this.adminStore.isLoading;
    },
    filteredUsers(): User[] {
      if (!this.searchQuery.trim()) {
        return this.users;
      }
      const query = this.searchQuery.toLowerCase();
      return this.users.filter(user =>
        user.name.toLowerCase().includes(query) ||
        user.email.toLowerCase().includes(query)
      );
    },
  },

  methods: {
    editUser(userId: number) {
      console.log('Editing user:', userId);
      // Логика открытия модального окна для редактирования
    },

    blockUser(userId: number) {
      if (confirm(`Are you sure you want to block user ID: ${userId}?`)) {
        this.adminStore.blockUser(userId); // Метод стора
      }
    },

    unblockUser(userId: number) {
      if (confirm(`Are you sure you want to unblock user ID: ${userId}?`)) {
        this.adminStore.unblockUser(userId); // Метод стора
      }
    },

    deleteUser(userId: number) {
      if (confirm(`DANGER: Are you sure you want to permanently delete user ID: ${userId}?`)) {
        this.adminStore.deleteUser(userId); // Метод стора
      }
    },
  },

  mounted() {
    this.adminStore.fetchUsers();
  },
});
</script>