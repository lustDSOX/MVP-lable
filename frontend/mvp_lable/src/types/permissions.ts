export type Permission =
  | 'releases.moderate'
  | 'news.manage'
  | 'events.manage'
  | 'guides.manage'
  | 'users.manage'
  | 'permissions.manage'

export const ALL_PERMISSIONS: { key: Permission; label: string }[] = [
  { key: 'releases.moderate', label: 'Релизы (очередь / approve)' },
  { key: 'news.manage', label: 'Новости CRUD' },
  { key: 'events.manage', label: 'Мероприятия CRUD' },
  { key: 'guides.manage', label: 'Гайды CRUD' },
  { key: 'users.manage', label: 'Пользователи' },
  { key: 'permissions.manage', label: 'Матрица доступа' },
]

export const ROLE_DEFAULTS: Record<string, Permission[]> = {
  artist: [],
  moderator: ['releases.moderate'],
  admin: [
    'releases.moderate',
    'news.manage',
    'events.manage',
    'guides.manage',
    'users.manage',
    'permissions.manage',
  ],
}
