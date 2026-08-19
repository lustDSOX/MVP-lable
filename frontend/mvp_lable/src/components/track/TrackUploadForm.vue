<template>
  <div class="border-2 border-[#333] bg-black p-4 sm:p-6 mt-6">
    <p v-if="specHint" class="mb-3 font-mono text-[10px] text-gray-500 uppercase">{{ specHint }}</p>
    <form @submit.prevent="submitTrack" class="space-y-6">
      <div>
        <label class="font-mono text-xs text-[#39FF14] uppercase">Cover (JPEG)</label>
        <input type="file" accept="image/jpeg,image/png,image/webp" required class="mt-2 block w-full text-sm text-gray-400" @change="onCoverChange" />
        <img v-if="coverPreviewUrl" :src="coverPreviewUrl" class="mt-2 w-32 h-32 object-cover border border-[#333]" alt="" />
      </div>
      <div>
        <label class="font-mono text-xs text-[#39FF14] uppercase">Audio (WAV/MP3) — mock: один файл на релиз</label>
        <input type="file" accept="audio/*" required class="mt-2 block w-full text-sm text-gray-400" @change="onWavChange" />
      </div>
      <button
        type="submit"
        :disabled="isLoading || !isFormValid"
        class="w-full bg-[#39FF14] text-black font-bold uppercase py-4 disabled:opacity-50 min-h-[52px]"
      >
        {{ isLoading ? '…' : 'Submit to moderation (mock)' }}
      </button>
    </form>
  </div>
</template>

<script lang="ts">
import { defineComponent } from 'vue'

export default defineComponent({
  name: 'TrackUploadForm',
  props: { trackId: { type: String, required: true } },
  emits: ['track-uploaded'],
  data() {
    return {
      wavFile: null as File | null,
      coverFile: null as File | null,
      coverPreviewUrl: null as string | null,
      isLoading: false,
    }
  },
  computed: {
    isFormValid(): boolean {
      return this.wavFile !== null && this.coverFile !== null
    },
    specHint(): string {
      try {
        const raw = sessionStorage.getItem(`release_draft_${this.trackId}`)
        if (!raw) return ''
        const m = JSON.parse(raw)
        return `Релиз: ${m.title || ''} · ${m.type || 'single'} · треков: ${m.trackCount || 1}`
      } catch {
        return ''
      }
    },
  },
  beforeUnmount() {
    if (this.coverPreviewUrl) URL.revokeObjectURL(this.coverPreviewUrl)
  },
  methods: {
    onCoverChange(e: Event) {
      const file = (e.target as HTMLInputElement).files?.[0] || null
      this.coverFile = file
      if (this.coverPreviewUrl) URL.revokeObjectURL(this.coverPreviewUrl)
      this.coverPreviewUrl = file ? URL.createObjectURL(file) : null
    },
    onWavChange(e: Event) {
      this.wavFile = (e.target as HTMLInputElement).files?.[0] || null
    },
    async submitTrack() {
      if (!this.isFormValid) return
      this.isLoading = true
      try {
        await new Promise((r) => setTimeout(r, 1000))
        this.$emit('track-uploaded', this.trackId)
      } finally {
        this.isLoading = false
      }
    },
  },
})
</script>
