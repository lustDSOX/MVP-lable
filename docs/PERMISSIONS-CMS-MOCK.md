# Permissions + CMS (front mock)

Статус: 2026-08-19. Без бэка, localStorage.

## Permissions
`releases.moderate` | `news.manage` | `events.manage` | `guides.manage` | `users.manage` | `permissions.manage`

Матрица: `/staff` (вкладка Access matrix). Admin = full.

## Demo
| email | password | rights |
|-------|----------|--------|
| moderator@label.ru | mod123 | releases |
| news@label.ru | news123 | news |
| events@label.ru | events123 | events |
| staff@label.ru | staff123 | releases+news+events |
| admin@label.ru | admin123 | all + matrix |

## Routes
- `/staff` — hub (CMS + matrix)
- `/moderator` — релизы (`releases.moderate`)
- `/news` `/events` — только published
