<template>
  <div class="ap border-2 border-[#333] bg-[#0a0a0a] p-3 sm:p-4 select-none">
    <div class="flex items-center gap-3 mb-3">
      <button
        type="button"
        class="ap-btn shrink-0"
        :aria-label="playing ? 'Pause' : 'Play'"
        @click="toggle"
      >
        <span v-if="!playing" class="ap-icon-play" />
        <span v-else class="ap-icon-pause" />
      </button>
      <div class="min-w-0 flex-1">
        <p class="font-mono text-[10px] uppercase text-[#39FF14] truncate">{{ title || 'TRACK' }}</p>
        <p v-if="subtitle" class="font-mono text-[9px] text-gray-500 truncate">{{ subtitle }}</p>
      </div>
      <span class="font-mono text-[10px] text-gray-400 tabular-nums shrink-0">
        {{ fmt(current) }} / {{ fmt(duration || 0) }}
      </span>
    </div>

    <div
      ref="barEl"
      class="ap-bar relative h-3 border border-[#333] bg-[#111] cursor-pointer"
      @click="seek"
      @keydown.left.prevent="nudge(-5)"
      @keydown.right.prevent="nudge(5)"
      role="slider"
      :aria-valuenow="Math.floor(current)"
      :aria-valuemin="0"
      :aria-valuemax="Math.floor(duration || 0)"
      tabindex="0"
    >
      <div class="absolute inset-y-0 left-0 bg-[#39FF14]" :style="{ width: pct + '%' }" />
      <div
        class="absolute top-1/2 -translate-y-1/2 w-3 h-3 bg-white border-2 border-black -ml-1.5"
        :style="{ left: pct + '%' }"
      />
    </div>

    <div class="flex items-center gap-2 mt-3">
      <button type="button" class="ap-sm" @click="nudge(-10)" aria-label="Back 10s">−10s</button>
      <button type="button" class="ap-sm" @click="nudge(10)" aria-label="Forward 10s">+10s</button>
      <div class="flex-1" />
      <button type="button" class="ap-sm w-9" @click="toggleMute" :aria-label="muted ? 'Unmute' : 'Mute'">
        {{ muted || volume === 0 ? '🔇' : '🔊' }}
      </button>
      <input
        type="range"
        min="0"
        max="1"
        step="0.01"
        :value="muted ? 0 : volume"
        class="ap-vol"
        @input="onVol"
        aria-label="Volume"
      />
    </div>

    <audio
      ref="audioEl"
      :src="src"
      preload="metadata"
      @timeupdate="onTime"
      @loadedmetadata="onMeta"
      @ended="onEnded"
      @play="playing = true"
      @pause="playing = false"
    />
  </div>
</template>

<script setup lang="ts">
import { computed, onBeforeUnmount, ref, watch } from 'vue'

const props = defineProps<{
  src: string
  title?: string
  subtitle?: string
}>()

const audioEl = ref<HTMLAudioElement | null>(null)
const barEl = ref<HTMLElement | null>(null)
const playing = ref(false)
const current = ref(0)
const duration = ref(0)
const volume = ref(0.9)
const muted = ref(false)

const pct = computed(() => (duration.value > 0 ? (current.value / duration.value) * 100 : 0))

function fmt(s: number) {
  if (!Number.isFinite(s) || s < 0) return '0:00'
  const m = Math.floor(s / 60)
  const sec = Math.floor(s % 60)
  return `${m}:${String(sec).padStart(2, '0')}`
}

function toggle() {
  const a = audioEl.value
  if (!a) return
  if (a.paused) void a.play()
  else a.pause()
}

function onTime() {
  current.value = audioEl.value?.currentTime || 0
}
function onMeta() {
  duration.value = audioEl.value?.duration || 0
  if (audioEl.value) audioEl.value.volume = volume.value
}
function onEnded() {
  playing.value = false
  current.value = 0
}

function seek(e: MouseEvent) {
  const a = audioEl.value
  const bar = barEl.value
  if (!a || !bar || !duration.value) return
  const rect = bar.getBoundingClientRect()
  const ratio = Math.min(1, Math.max(0, (e.clientX - rect.left) / rect.width))
  a.currentTime = ratio * duration.value
  current.value = a.currentTime
}

function nudge(sec: number) {
  const a = audioEl.value
  if (!a) return
  a.currentTime = Math.min(duration.value || a.duration || 0, Math.max(0, a.currentTime + sec))
}

function toggleMute() {
  const a = audioEl.value
  if (!a) return
  muted.value = !muted.value
  a.muted = muted.value
}

function onVol(e: Event) {
  const v = Number((e.target as HTMLInputElement).value)
  volume.value = v
  muted.value = v === 0
  if (audioEl.value) {
    audioEl.value.volume = v
    audioEl.value.muted = muted.value
  }
}

watch(
  () => props.src,
  () => {
    playing.value = false
    current.value = 0
    duration.value = 0
  },
)

onBeforeUnmount(() => {
  audioEl.value?.pause()
})
</script>

<style scoped>
.ap-btn {
  width: 48px;
  height: 48px;
  min-width: 48px;
  background: #39ff14;
  color: #000;
  border: 2px solid #000;
  display: flex;
  align-items: center;
  justify-content: center;
  box-shadow: 3px 3px 0 #ff0000;
}
.ap-btn:active {
  transform: translate(1px, 1px);
  box-shadow: 1px 1px 0 #ff0000;
}
.ap-icon-play {
  width: 0;
  height: 0;
  border-style: solid;
  border-width: 8px 0 8px 14px;
  border-color: transparent transparent transparent #000;
  margin-left: 3px;
}
.ap-icon-pause {
  width: 14px;
  height: 14px;
  background: linear-gradient(to right, #000 0 5px, transparent 5px 9px, #000 9px 14px);
}
.ap-sm {
  font-family: 'JetBrains Mono', monospace;
  font-size: 10px;
  text-transform: uppercase;
  padding: 0.35rem 0.5rem;
  min-height: 36px;
  border: 1px solid #333;
  color: #aaa;
  background: #111;
}
.ap-sm:hover {
  border-color: #39ff14;
  color: #39ff14;
}
.ap-vol {
  width: 72px;
  accent-color: #39ff14;
  height: 4px;
}
.ap-bar:focus-visible {
  outline: 2px solid #39ff14;
  outline-offset: 2px;
}
</style>
