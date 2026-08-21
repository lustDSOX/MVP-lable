import { defineStore } from 'pinia'
import type { ReleaseType, ContributorInput } from '@/types/release'

export type TrackStatus = 'draft' | 'pending' | 'approved' | 'published' | 'rejected' | 'changes_requested'

export type HistoryKind = 'moderation' | 'artist_edit' | 'contract' | 'submit' | 'system'

export interface PlatformStats {
  spotify: number
  apple: number
  yandex: number
  vk: number
}

export interface PlatformFollowers {
  spotify: number
  apple: number
  yandex: number
  vk: number
}

export interface ReleaseTrackDetail {
  localId: string
  title: string
  order: number
  isExplicit: boolean
  lyrics: string
  masterFile?: string
  previewFile?: string
  audioUrl?: string
  plays?: number
  genres?: string[]
  contributors: ContributorInput[]
}

export interface ContractInfo {
  signed: boolean
  signedAt?: string
  version: string
  artistFullName: string
  status: 'unsigned' | 'signed' | 'void' | 'needs_resign'
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
  followers?: PlatformFollowers
  createdAt: string
  type?: ReleaseType
  genre?: string
  genres?: string[]
  releaseDate?: string
  artistName?: string
  artistEmail?: string
  artistPhone?: string
  artistCity?: string
  socialNetworks?: string
  coverNote?: string
  coverUrl?: string
  contractPdfUrl?: string
  tracksDetail?: ReleaseTrackDetail[]
  contract?: ContractInfo
  moderationLog?: { at: string; action: string; by: string; note?: string; kind?: HistoryKind }[]
  liveRevision?: boolean
  changeRequestNote?: string
}

const COVER = 'https://picsum.photos/seed/mvp-cover/600/600'
const PDF = 'https://www.w3.org/WAI/ER/tests/xhtml/testfiles/resources/pdf/dummy.pdf'
const AUDIO = 'https://www.soundhelix.com/examples/mp3/SoundHelix-Song-1.mp3'

export const useTracksStore = defineStore('tracks', {
  state: () => ({
    tracks: [] as Track[],
    isLoading: false,
  }),
  getters: {
    totalPlays: (state) => state.tracks.reduce((sum, t) => sum + t.plays, 0),
    totalRoyalties: (state) => state.tracks.reduce((sum, t) => sum + t.royalties, 0),
    byStatus: (state) => (status: TrackStatus) => state.tracks.filter((t) => t.status === status),
  },
  actions: {
    async fetchTracks() {
      this.isLoading = true
      await new Promise((r) => setTimeout(r, 400))
      this.tracks = [
        {
          id: '1',
          title: 'Cyber City',
          status: 'published',
          plays: 12500,
          royalties: 450.5,
          contractSigned: true,
          platforms: { spotify: 5200, apple: 3100, yandex: 2800, vk: 1400 },
          followers: { spotify: 890, apple: 420, yandex: 610, vk: 1200 },
          createdAt: '2026-01-10',
          type: 'single',
          genre: 'electronic',
          genres: ['electronic', 'synthwave'],
          releaseDate: '2026-01-15',
          artistName: 'DJ Neon',
          artistEmail: 'demo@label.ru',
          artistPhone: '+7 900 000-00-00',
          artistCity: 'Moscow',
          socialNetworks: '@djneon',
          coverNote: '3000x3000 RGB',
          coverUrl: COVER,
          contractPdfUrl: PDF,
          tracksDetail: [
            {
              localId: 't1',
              title: 'Cyber City',
              order: 1,
              isExplicit: false,
              lyrics: 'Neon veins under glass rain...\nGrid runner, midnight lane.',
              masterFile: 'cyber_city_master.wav',
              audioUrl: AUDIO,
              plays: 12500,
              genres: ['electronic', 'synthwave'],
              contributors: [
                { role: 'main_artist', creditName: 'DJ Neon' },
                { role: 'producer', creditName: 'Void Lab' },
              ],
            },
          ],
          contract: { signed: true, signedAt: '2026-01-09T18:00:00Z', version: 'v0.3', artistFullName: 'Ivan Ivanov', status: 'signed' },
          moderationLog: [{ at: '2026-01-10T10:00:00Z', action: 'approved', by: 'moderator@label.ru', kind: 'moderation' }],
        },
        {
          id: '2',
          title: 'Neon Lights',
          status: 'rejected',
          plays: 0,
          royalties: 0,
          rejectReason: 'Cover art resolution too low · lyrics incomplete on track 1',
          contractSigned: true,
          platforms: { spotify: 0, apple: 0, yandex: 0, vk: 0 },
          followers: { spotify: 0, apple: 0, yandex: 0, vk: 0 },
          createdAt: '2026-02-01',
          type: 'single',
          genre: 'synthwave',
          genres: ['synthwave'],
          releaseDate: '2026-02-20',
          artistName: 'DJ Neon',
          artistEmail: 'demo@label.ru',
          artistPhone: '+7 900 000-00-00',
          artistCity: 'Moscow',
          socialNetworks: '@djneon',
          coverNote: '1500x1500 (INVALID)',
          coverUrl: COVER,
          contractPdfUrl: PDF,
          tracksDetail: [
            {
              localId: 't1',
              title: 'Neon Lights',
              order: 1,
              isExplicit: true,
              lyrics: '[explicit verse]\nLights cut through the fog...',
              masterFile: 'neon_lights.wav',
              audioUrl: AUDIO,
              plays: 0,
              genres: ['synthwave'],
              contributors: [{ role: 'main_artist', creditName: 'DJ Neon' }],
            },
          ],
          contract: { signed: true, signedAt: '2026-01-28T12:00:00Z', version: 'v0.3', artistFullName: 'Ivan Ivanov', status: 'signed' },
          moderationLog: [
            { at: '2026-01-28T10:00:00Z', action: 'draft_saved', by: 'demo@label.ru', kind: 'artist_edit', note: 'First draft' },
            { at: '2026-02-01T12:00:00Z', action: 'submitted', by: 'demo@label.ru', kind: 'submit' },
            { at: '2026-02-02T09:00:00Z', action: 'rejected', by: 'moderator@label.ru', kind: 'moderation', note: 'Cover art resolution too low · lyrics incomplete on track 1' },
          ],
        },
        {
          id: '3',
          title: 'Grid Runner EP',
          status: 'pending',
          plays: 9100,
          royalties: 0,
          contractSigned: true,
          platforms: { spotify: 4100, apple: 2200, yandex: 1800, vk: 1000 },
          followers: { spotify: 320, apple: 150, yandex: 280, vk: 540 },
          createdAt: '2026-03-15',
          type: 'ep',
          genre: 'bass / experimental',
          genres: ['bass', 'experimental'],
          releaseDate: '2026-04-01',
          artistName: 'DJ Neon',
          artistEmail: 'demo@label.ru',
          artistPhone: '+7 900 000-00-00',
          artistCity: 'Moscow',
          socialNetworks: '@djneon',
          coverNote: '3000x3000 OK',
          coverUrl: COVER,
          contractPdfUrl: PDF,
          tracksDetail: [
            {
              localId: 't1',
              title: 'Grid Runner',
              order: 1,
              isExplicit: false,
              lyrics: 'Run the grid, break the wall...',
              masterFile: 'grid_runner.wav',
              audioUrl: AUDIO,
              plays: 4200,
              genres: ['bass'],
              contributors: [
                { role: 'main_artist', creditName: 'DJ Neon' },
                { role: 'featured', creditName: 'Kai' },
              ],
            },
            {
              localId: 't2',
              title: 'Sector 7',
              order: 2,
              isExplicit: false,
              lyrics: 'Sector seven, signal lost...',
              masterFile: 'sector_7.wav',
              audioUrl: AUDIO,
              plays: 3100,
              genres: ['experimental'],
              contributors: [
                { role: 'main_artist', creditName: 'DJ Neon' },
                { role: 'producer', creditName: 'Lab Unit' },
              ],
            },
            {
              localId: 't3',
              title: 'Exit Ramp',
              order: 3,
              isExplicit: true,
              lyrics: '[explicit]\nExit ramp at dawn...',
              masterFile: 'exit_ramp.wav',
              audioUrl: AUDIO,
              plays: 1800,
              genres: ['bass', 'experimental'],
              contributors: [{ role: 'main_artist', creditName: 'DJ Neon' }],
            },
          ],
          contract: { signed: true, signedAt: '2026-03-14T20:00:00Z', version: 'v0.3', artistFullName: 'Ivan Ivanov', status: 'signed' },
          moderationLog: [{ at: '2026-03-15T08:00:00Z', action: 'submitted', by: 'demo@label.ru', kind: 'submit' }],
        },
      ]
      this.isLoading = false
    },
    createFromRelease(meta: { title: string; trackCount?: number; type?: string }) {
      const newTrack: Track = {
        id: Date.now().toString(),
        title: meta.title || 'New release',
        status: 'draft',
        plays: 0,
        royalties: 0,
        contractSigned: true,
        platforms: { spotify: 0, apple: 0, yandex: 0, vk: 0 },
        followers: { spotify: 0, apple: 0, yandex: 0, vk: 0 },
        createdAt: new Date().toISOString().slice(0, 10),
        type: (meta.type as ReleaseType) || 'single',
        tracksDetail: [],
        contract: { signed: true, signedAt: new Date().toISOString(), version: 'v0.3', artistFullName: '-', status: 'signed' },
        moderationLog: [],
      }
      this.tracks.unshift(newTrack)
      return newTrack.id
    },
    createDraftContract(title: string) {
      return this.createFromRelease({ title, trackCount: 1 })
    },
    completeTrackUpload(id: string) {
      const track = this.tracks.find((t) => t.id === id)
      if (track) {
        if (track.status === 'published' || track.liveRevision) track.liveRevision = true
        track.status = 'pending'
        track.rejectReason = undefined
        track.changeRequestNote = undefined
        track.moderationLog = track.moderationLog || []
        track.moderationLog.push({
          at: new Date().toISOString(),
          action: track.liveRevision ? 'resubmit_live' : 'submitted',
          by: 'artist',
          kind: 'submit',
          note: track.liveRevision ? 'Update of already published release' : undefined,
        })
      }
    },
    setStatus(id: string, status: TrackStatus, reason?: string, by = 'moderator') {
      const track = this.tracks.find((t) => t.id === id)
      if (!track) return
      track.status = status
      if (status === 'rejected' || status === 'changes_requested') {
        track.rejectReason = reason || (status === 'changes_requested' ? 'Changes required' : 'Rejected')
        if (status === 'changes_requested') track.changeRequestNote = reason
      } else {
        track.rejectReason = undefined
        track.changeRequestNote = undefined
      }
      if (status === 'published') track.liveRevision = false
      track.moderationLog = track.moderationLog || []
      track.moderationLog.push({ at: new Date().toISOString(), action: status, by, note: reason, kind: 'moderation' })
    },
    requestChanges(id: string, note: string, by = 'moderator') {
      this.setStatus(id, 'changes_requested', note, by)
    },
    pushHistory(id: string, action: string, by: string, note?: string, kind: HistoryKind = 'system') {
      const track = this.tracks.find((t) => t.id === id)
      if (!track) return
      track.moderationLog = track.moderationLog || []
      track.moderationLog.push({ at: new Date().toISOString(), action, by, note, kind })
    },
    updateRelease(
      id: string,
      patch: Partial<Track> & { tracksDetail?: Track['tracksDetail'] },
      by = 'artist',
    ): { needsResign: boolean } {
      const track = this.tracks.find((t) => t.id === id)
      if (!track) return { needsResign: false }
      const wasPublished = track.status === 'published' || !!track.liveRevision
      const sensitive =
        (patch.title !== undefined && patch.title !== track.title) ||
        (patch.type !== undefined && patch.type !== track.type) ||
        (patch.tracksDetail !== undefined &&
          JSON.stringify(patch.tracksDetail) !== JSON.stringify(track.tracksDetail))
      Object.assign(track, {
        ...patch,
        id: track.id,
        platforms: patch.platforms || track.platforms,
        moderationLog: track.moderationLog,
      })
      if (sensitive) {
        if (track.contract) {
          track.contract.signed = false
          track.contract.status = 'needs_resign'
          track.contractSigned = false
        }
        if (wasPublished) {
          track.liveRevision = true
          track.status = 'pending'
          this.pushHistory(id, 'live_edit_pending', by, 'Published release edits need moderation after re-sign', 'artist_edit')
        } else if (track.status === 'pending') {
          this.pushHistory(id, 'artist_edit_sensitive', by, 'Edits during moderation need re-sign', 'artist_edit')
        } else {
          track.status = track.status === 'changes_requested' ? 'draft' : track.status
          this.pushHistory(id, 'artist_edit_sensitive', by, 'Edits require contract re-sign', 'artist_edit')
        }
        return { needsResign: true }
      }
      if (wasPublished && track.status === 'published) {
        track.liveRevision = true
        track.status = 'pending'
        this.pushHistory(id, 'live_edit_pending', by, 'Published release edits under review', 'artist_edit')
        return { needsResign: false }
      }
      this.pushHistory(id, 'artist_edit', by, 'Release edits saved', 'artist_edit')
      return { needsResign: false }
    },
    resignContract(id: string, fullName: string, by = 'artist') {
      const track = this.tracks.find((t) => t.id === id)
      if (!track) return
      track.contract = {
        signed: true,
        signedAt: new Date().toISOString(),
        version: track.contract?.version || 'v0.3',
        artistFullName: fullName,
        status: 'signed',
      }
      track.contractSigned = true
      this.pushHistory(id, 'contract_resigned', by, fullName, 'contract')
    },
    requeue(id: string, by = 'moderator') {
      this.setStatus(id, 'pending', undefined, by)
    },
  },
})
