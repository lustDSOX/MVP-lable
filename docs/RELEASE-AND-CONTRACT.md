# Релиз, треки и договор — модель продукта

Статус: 2026-08-19. Источник правды для фронта и бэка.

## Принципы

1. **Профиль артиста** в `User` / profile. В форме релиза ФИО, email, alias — **read-only** (снимок для договора).
2. **Релиз** (`Release`) — единица публикации: `single` | `ep` | `album`.
3. **Треки** (`Track[]`) у релиза; contributors (feat, producer, …) **на каждый трек**.
4. **Договор** — **один на релиз** (или сделку артист↔лейбл), не на каждый трек. Треклист — спецификация к договору.
5. Файлы (cover, master/preview) — после подписания, по `release_id` / `track_id`.

## Сущности

```
User (profile)
  └── Release (type, title, genre, release_date, status, cover)
        ├── Contract (status: draft|sent|signed, file_url)
        ├── Track[] (title, order, explicit, lyrics, files)
        │     └── TrackContributor[] (role, user_id?, credit_name)
        └── ReleaseLink[] (platform, url)
```

### Release.type
| type | tracks |
|------|--------|
| `single` | 1 |
| `ep` | 2–6 (UI soft) |
| `album` | 7+ (UI soft) |

Статусы релиза: `draft → pending → approved|rejected → published`.

## API (цель)

```
POST /releases                 { type, title, genre, release_date }
POST /releases/{id}/tracks     { title, order, is_explicit, lyrics, contributors[] }
POST /contracts                { release_id } → PDF
POST /contracts/{id}/sign
POST /releases/{id}/submit
POST /files/upload
```

Roles contributors: `main_artist | featured | producer | songwriter | other`.

## Не делать

- Не собирать ФИО/email с нуля каждый релиз при логине.
- Не договор на каждый трек альбома.
- Не одна строка `coAuthors` — только structured contributors.

См. также BACKEND-ROADMAP.md.
