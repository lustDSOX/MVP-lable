export type Permission =
  | 'releases.moderate'
  | 'news.manage'
  | 'events.manage'
  | 'guides.manage'
  | 'users.manage'
  | 'permissions.manage'

export type SystemRole = 'artist' | 'moderator' | 'admin' | 'news_editor' | 'events_editor'

export const ALL_PERMISSIONS: { key: Permission; label: string }[] = [
  { key: 'releases.moderate', label: 'Релизы' },
  { key: 'news.manage', label: 'Новости' },
  { key: 'events.manage', label: 'События' },
  { key: 'guides.manage', label: 'Гайды' },
  { key: 'users.manage', label: 'Аккаунты' },
  { key: 'permissions.manage', label: 'Матрица ролей' },
]

export const ALL_ROLES: { key: SystemRole; label: string }[] = [
  { key: 'artist', label: 'Артист' },
  { key: 'moderator', label: 'Модератор релизов' },
  { key: 'news_editor', label: 'Редактор новостей' },
  { key: 'events_editor', label: 'Редактор событий' },
  { key: 'admin', label: 'Админ' },
]

export const ROLE_DEFAULTS: Record<SystemRole, Permission[]> = {
  artist: [],
  moderator: ['releases.moderate'],
  news_editor: ['news.manage'],
  events_editor: ['events.manage'],
  admin: [
    'releases.moderate',
    'news.manage',
    'events.manage',
    'guides.manage',
    'users.manage',
    'permissions.manage',
  ],
}
