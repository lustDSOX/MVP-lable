<template>
  <section class="mb-6 border-2 border-[#333] bg-[#0a0a0a] p-4 sm:p-6">
    <div class="flex flex-wrap items-center justify-between gap-2 mb-4">
      <h2 class="font-mono text-sm uppercase tracking-widest text-[#39FF14]">Platform_Links // MOCK</h2>
      <span class="font-mono text-[10px] text-gray-500">{{ platformsStore.connectedCount }}/4 connected</span>
    </div>
    <div class="grid grid-cols-1 sm:grid-cols-2 gap-3">
      <div
        v-for="acc in platformsStore.accounts"
        :key="acc.id"
        class="border border-[#333] p-3 flex items-center justify-between gap-3"
      >
        <div>
          <p class="font-mono text-xs uppercase text-white">{{ acc.label }}</p>
          <p class="font-mono text-[10px] text-gray-500 mt-1">
            {{ acc.connected ? acc.accountName : 'not linked' }}
          </p>
        </div>
        <button
          type="button"
          class="min-h-[44px] px-3 font-mono text-[10px] uppercase border-2 shrink-0"
          :class="acc.connected ? 'border-[#ff0000] text-[#ff0000]' : 'border-[#39FF14] text-[#39FF14]'"
          :disabled="platformsStore.busyId === acc.id"
          @click="acc.connected ? platformsStore.disconnect(acc.id) : platformsStore.connect(acc.id)"
        >
          {{ platformsStore.busyId === acc.id ? '…' : acc.connected ? 'Disconnect' : 'Connect' }}
        </button>
      </div>
    </div>
    <p class="mt-3 font-mono text-[9px] text-gray-600 uppercase">OAuth later · localStorage mock now</p>
  </section>
</template>

<script setup lang="ts">
import { onMounted } from 'vue'
import { usePlatformsStore } from '@/stores/platforms'

const platformsStore = usePlatformsStore()
onMounted(() => platformsStore.hydrate())
</script>
