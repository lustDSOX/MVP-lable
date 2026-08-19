import { defineStore } from 'pinia'

export type TrackStatus = 'draft' | 'pending' | 'approved' | 'published' | 'rejected'

export interface PlatformStats {
  spotify: number
  apple: number
  yandex: number
  vk: number
}

export interface Track {
  id: string
  title: string
  status: TrackStatus
  plays: number
  royalties: number
  rejectReason?: string
  contractSigned: boolean
  platforms: PlatformStats
  createdAt: string
}

export const useTracksStore = defineStore('tracks', {
  state: () => ({
    tracks: [] as Track[],
    isLoading: false,
  }),

  getters: {
    totalPlays: (state) => state.tracks.reduce((sum, t) => sum + t.plays, 0),
    totalRoyalties: (state) => state.tracks.reduce((sum, t) => sum + t.royalties, 0),
    byStatus: (state) => (status: TrackStatus) =>
      state.tracks.filter((t) => t.status === status),
  },

  actions: {
    async fetchTracks() {
      this.isLoading = true
      await new Promise((r) => setTimeout(r, 600))
      this.tracks = [
        {
          id: '1',
          title: 'Cyber City',
          status: 'published',
          plays: 12500,
          royalties: 450.5,
          contractSigned: true,
          platforms: { spotify: 5200, apple: 3100, yandex: 2800, vk: 1400 },
          createdAt: '2026-01-10',
        },
        {
          id: '2',
          title: 'Neon Lights',
          status: 'rejected',
          plays: 0,
          royalties: 0,
          rejectReason: 'Обложка не 3000×3000',
          contractSigned: true,
          platforms: { spotify: 0, apple: 0, yandex: 0, vk: 0 },
          createdAt: '2026-02-01',
        },
        {
          id: '3',
          title: 'Grid Runner EP',
          status: 'pending',
          plays: 0,
          royalties: 0,
          contractSigned: true,
          platforms: { spotify: 0, apple: 0, yandex: 0, vk: 0 },
          createdAt: '2026-03-15',
        },
      ]
      this.isLoading = false
    },

    createDraftContract(title: string) {
      const newTrack: Track = {
        id: Date.now().toString(),
        title: title || 'Новый релиз',
        status: 'draft',
        plays: 0,
        royalties: 0,
        contractSigned: true,
        platforms: { spotify: 0, apple: 0, yandex: 0, vk: 0 },
        createdAt: new Date().toISOString().slice(0, 10),
      }
      this.tracks.unshift(newTrack)
      return newTrack.id
    },

    completeTrackUpload(id: string) {
      const track = this.tracks.find((t) => t.id === id)
      if (track) {
        track.status = 'pending'
        track.rejectReason = undefined
      }
    },

    setStatus(id: string, status: TrackStatus, reason?: string) {
      const track = this.tracks.find((t) => t.id === id)
      if (!track) return
      track.status = status
      if (status === 'rejected') track.rejectReason = reason || 'Rejected'
      else track.rejectReason = undefined
    },
  },
})
