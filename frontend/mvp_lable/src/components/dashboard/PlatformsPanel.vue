<template>
  <section class="mb-6 border-2 border-[#333] bg-[#0a0a0a] p-4 sm:p-6">
    <div class="flex flex-wrap items-center justify-between gap-2 mb-4">
      <h2 class="font-mono text-sm uppercase tracking-widest text-[#39FF14]">Platform_Links // MOCK</h2>
      <span class="font-mono text-[10px] text-gray-500">{{ platformsStore.connectedCount }}/4 connected</span>
    </div>
    <div class="grid grid-cols-1 sm:grid-cols-2 gap-3">
      <div
        v-for="row in platformRows"
        :key="row.id"
        class="border border-[#333] p-3 space-y-2"
        :class="{ 'opacity-50': !row.connected }"
      >
        <div class="flex items-center justify-between gap-3">
          <div>
            <p class="font-mono text-xs uppercase text-white">{{ row.label }}</p>
            <p class="font-mono text-[10px] text-gray-500 mt-1">
              {{ row.connected ? row.accountName : 'not linked' }}
            </p>
          </div>
          <button
            type="button"
            class="min-h-[44px] px-3 font-mono text-[10px] uppercase border-2 shrink-0"
            :class="row.connected ? 'border-[#ff0000] text-[#ff0000]' : 'border-[#39FF14] text-[#39FF14]'"
            :disabled="platformsStore.busyId === row.id"
            @click="row.connected ? platformsStore.disconnect(row.id) : platformsStore.connect(row.id)"
          >
            {{ platformsStore.busyId === row.id ? '…' : row.connected ? 'Disconnect' : 'Connect' }}
          </button>
        </div>
        <div class="flex justify-between font-mono text-[10px]">
          <span class="text-gray-600">Прослушивания</span>
          <span class="text-white">{{ row.plays.toLocaleString() }}</span>
        </div>
        <div class="flex justify-between font-mono text-[10px]">
          <span class="text-gray-600">Подписчики</span>
          <span class="text-[#39FF14]">{{ row.followers.toLocaleString() }}</span>
        </div>
      </div>
    </div>
    <p class="mt-3 font-mono text-[9px] text-gray-600 uppercase">OAuth later · localStorage mock now</p>
  </section>
</template>

<script setup lang="ts">
import { computed, onMounted } from 'vue'
import { usePlatformsStore } from '@/stores/platforms'
import { useTracksStore } from '@/stores/tracks'

const platformsStore = usePlatformsStore()
const tracksStore = useTracksStore()
onMounted(() => platformsStore.hydrate())

const platformRows = computed(() => {
  return platformsStore.accounts.map((acc) => {
    const plays = tracksStore.tracks.reduce((s, tr) => s + (tr.platforms?.[acc.id] ?? 0), 0)
    const followers = tracksStore.tracks.reduce((s, tr) => s + (tr.followers?.[acc.id] ?? 0), 0)
    return {
      id: acc.id,
      label: acc.label,
      connected: acc.connected,
      accountName: acc.accountName,
      plays,
      followers,
    }
  })
})
</script>
