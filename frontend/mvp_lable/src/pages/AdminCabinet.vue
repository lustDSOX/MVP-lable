<!-- AdminCabinet.vue -->
<template>
  <div class="min-h-screen pt-24 px-4 pb-12 font-['Inter',sans-serif] text-white relative">
    <div class="max-w-7xl mx-auto flex flex-col gap-12 relative z-10">

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

      <section class="data-panel-container">
        <div class="data-panel-content">
          <div class="stat-item">
            <span class="label">Total Users</span>
            <span class="value">{{ users.length }}</span>
          </div>
          <div class="stat-item">
            <span class="label">Monthly Active</span>
            <span class="value">0</span>
          </div>
          <div class="stat-item">
            <span class="label">Blocked Users</span>
            <span class="value">{{ users.filter(u => u.status === 'blocked').length }}</span>
          </div>
        </div>
      </section>

      <section class="bg-black border border-[#333]">
        <!-- Mobile user cards -->
        <div class="md:hidden space-y-3 p-3">
          <article
            v-for="user in filteredUsers"
            :key="'m-' + user.id"
            class="border-2 border-[#333] bg-[#0a0a0a] p-4 flex flex-col gap-3"
          >
            <div class="flex justify-between gap-2 items-start">
              <div class="min-w-0">
                <h3 class="font-bold text-white uppercase text-sm leading-tight">{{ user.name }}</h3>
                <p class="text-xs text-gray-500 font-mono truncate mt-1">{{ user.email }}</p>
              </div>
              <span class="text-[10px] font-mono uppercase shrink-0 border border-[#444] px-2 py-0.5">{{ user.status }}</span>
            </div>
            <p class="text-xs text-gray-600 font-mono">Reg: {{ user.registered_at ? new Date(user.registered_at).toLocaleDateString() : '—' }}</p>
            <div class="flex gap-2">
              <button type="button" v-if="user.status !== 'blocked'" @click="blockUser(user.id)" class="flex-1 min-h-[44px] border-2 border-[#333] text-xs font-mono uppercase">Block</button>
              <button type="button" v-else @click="unblockUser(user.id)" class="flex-1 min-h-[44px] border-2 border-[#39FF14] text-[#39FF14] text-xs font-mono uppercase">Unblock</button>
              <button type="button" @click="deleteUser(user.id)" class="flex-1 min-h-[44px] border-2 border-[#ff0000] text-[#ff0000] text-xs font-mono uppercase">Delete</button>
            </div>
          </article>
          <p v-if="!filteredUsers.length && !isLoading" class="text-center text-gray-600 py-8 font-mono text-sm">NO_USERS</p>
          <p v-if="isLoading" class="text-center text-[#ff0000] py-8 font-mono text-sm animate-pulse">LOADING...</p>
        </div>

        <div class="overflow-x-auto hidden md:block">
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
                     <button @click="editUser(user.id)" class="action-button" title="Edit User Data">Edit</button>
                     <button v-if="user.status === 'active'" @click="blockUser(user.id)" class="action-button" title="Block User">Block</button>
                     <button v-else @click="unblockUser(user.id)" class="action-button" title="Unblock User">Unblock</button>
                     <button @click="deleteUser(user.id)" class="action-button delete-button" title="Delete User">Del</button>
                  </div>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </section>
    </div>
  </div>
</template>

<style scoped>
.action-button.delete-button:hover {
    background-color: #ff0000;
    color: white;
}
.command-center-grid {
  display: grid;
  grid-template-columns: 1fr;
  gap: 1.5rem;
}
@media (min-width: 1024px) {
  .command-center-grid {
    grid-template-columns: 1fr 380px;
    align-items: end;
  }
  .welcome-block { grid-column: 1 / -1; }
}
.welcome-subtitle {
  font-family: 'JetBrains Mono', monospace;
  font-size: 10px;
  color: #6b7280;
  text-transform: uppercase;
  letter-spacing: 0.4em;
  margin-top: 0.5rem;
  display: block;
}
.search-input {
  width: 100%;
  background-color: black;
  border: 2px solid #333;
  padding: 1rem;
  font-family: 'JetBrains Mono', monospace;
  color: white;
  text-transform: uppercase;
}
.upload-button {
  width: 100%;
  padding: 1rem;
  background-color: white;
  color: black;
  border: 4px solid black;
  text-transform: uppercase;
  box-shadow: 4px 4px 0 #ff0000;
  font-family: 'Archivo Black', sans-serif;
  position: relative;
  overflow: hidden;
}
.data-panel-container { border: 2px solid #333; background: black; }
.data-panel-content {
  display: grid;
  grid-template-columns: 1fr;
  gap: 1px;
  background: #333;
}
@media (min-width: 768px) {
  .data-panel-content { grid-template-columns: repeat(3, 1fr); }
}
.stat-item { background: black; padding: 1.5rem; }
.stat-item .label {
  font-family: 'JetBrains Mono', monospace;
  font-size: 0.875rem;
  color: #6b7280;
  text-transform: uppercase;
}
.stat-item .value {
  font-family: 'Archivo Black', sans-serif;
  font-size: 2rem;
}
.table-header { border-bottom: 2px solid #333; }
.table-th {
  padding: 1rem;
  text-transform: uppercase;
  font-family: 'JetBrains Mono', monospace;
  font-size: 0.875rem;
  color: #6b7280;
}
.table-row { border-bottom: 1px solid #222; }
.track-title {
  font-family: 'Archivo Black', sans-serif;
  font-size: 1.1rem;
  text-transform: uppercase;
}
.status-badge {
  font-family: 'JetBrains Mono', monospace;
  font-weight: 700;
  font-size: 0.75rem;
  padding: 0.25rem 0.5rem;
  text-transform: uppercase;
}
.status-online { background-color: #39FF14; color: black; }
.status-error { background-color: #ff0000; color: white; }
.action-button {
  background-color: #222;
  color: #9ca3af;
  padding: 0.5rem 0.75rem;
  font-size: 0.75rem;
  text-transform: uppercase;
}
.crt-noise {
  background-image: url('data:image/svg+xml;utf8,%3Csvg viewBox="0 0 200 200" xmlns="http://www.w3.org/2000/svg"%3E%3Cfilter id="n"%3E%3CfeTurbulence type="fractalNoise" baseFrequency="0.9" numOctaves="3"/%3E%3C/filter%3E%3Crect width="100%25" height="100%25" filter="url(%23n)"/%3E%3C/svg%3E');
}
</style>

<script lang="ts">
import { defineComponent } from 'vue';
import { useAuthStore } from '@/stores/auth';
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
      return this.adminStore.users;
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
    },

    blockUser(userId: number) {
      if (confirm(`Are you sure you want to block user ID: ${userId}?`)) {
        this.adminStore.blockUser(userId);
      }
    },

    unblockUser(userId: number) {
      if (confirm(`Are you sure you want to unblock user ID: ${userId}?`)) {
        this.adminStore.unblockUser(userId);
      }
    },

    deleteUser(userId: number) {
      if (confirm(`DANGER: Are you sure you want to permanently delete user ID: ${userId}?`)) {
        this.adminStore.deleteUser(userId);
      }
    },
  },

  mounted() {
    this.adminStore.fetchUsers();
  },
});
</script>
