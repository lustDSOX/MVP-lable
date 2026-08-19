import type { ReleaseDraft } from './release'

/** @deprecated use ReleaseDraft — legacy flat form */
export interface ContractFormData {
  fullName: string
  email: string
  phone: string
  nicknames: string
  socialNetworks: string
  genre: string
  age: number | null
  city: string
  trackTitle: string
  coAuthors: string
}

export interface ContractPackage {
  release: ReleaseDraft
  pdfUrl?: string
  signed: boolean
}
