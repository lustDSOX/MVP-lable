/** Shared front+back contract for release upload pipeline */

export type ReleaseType = 'single' | 'ep' | 'album'

export type ContributorRole =
  | 'main_artist'
  | 'featured'
  | 'producer'
  | 'songwriter'
  | 'other'

export interface ContributorInput {
  role: ContributorRole
  userId?: number | null
  creditName: string
}

export interface TrackInput {
  localId: string
  title: string
  order: number
  isExplicit: boolean
  lyrics: string
  masterFile?: string
  previewFile?: string
  contributors: ContributorInput[]
}

export interface ArtistProfileSnapshot {
  fullName: string
  email: string
  phone: string
  artistName: string
  socialNetworks: string
  age: number | null
  city: string
}

export interface ReleaseDraft {
  type: ReleaseType
  title: string
  genre: string
  releaseDate: string
  contractRequired: true
  profile: ArtistProfileSnapshot
  tracks: TrackInput[]
}
