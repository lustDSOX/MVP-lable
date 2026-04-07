import { defineStore } from 'pinia'

// Возможные статусы релиза
export type TrackStatus = 'draft' | 'moderation' | 'published' | 'rejected'

export interface Track {
  id: string
  title: string
  status: TrackStatus
  plays: number
  royalties: number
  rejectReason?: string // Если статус rejected
}

export const useTracksStore = defineStore('tracks', {
  state: () => ({
    tracks: [] as Track[],
    isLoading: false
  }),

  getters: {
    totalPlays: (state) => state.tracks.reduce((sum, track) => sum + track.plays, 0),
    totalRoyalties: (state) => state.tracks.reduce((sum, track) => sum + track.royalties, 0)
  },

  actions: {
    async fetchTracks() {
      this.isLoading = true
      // Заглушка API
      await new Promise(res => setTimeout(res, 1000))
      this.tracks = [
        { id: '1', title: 'Cyber City', status: 'published', plays: 12500, royalties: 450.50 },
        { id: '2', title: 'Neon Lights', status: 'rejected', plays: 0, royalties: 0, rejectReason: 'Обложка не соответствует требованиям площадок (нужно 3000x3000px)' }
      ]
      this.isLoading = false
    },

    // Вызывается после успешного подписания договора в модалке
    createDraftContract(title: string) {
      const newTrack: Track = {
        id: Date.now().toString(),
        title: title || 'Новый релиз (без названия)',
        status: 'draft',
        plays: 0,
        royalties: 0
      }
      this.tracks.unshift(newTrack) // Добавляем в начало списка
      return newTrack.id
    },

    // Вызывается после загрузки WAV и Обложки
    completeTrackUpload(id: string) {
      const track = this.tracks.find(t => t.id === id)
      if (track) {
        track.status = 'moderation'
        track.rejectReason = undefined
      }
    }
  }
})