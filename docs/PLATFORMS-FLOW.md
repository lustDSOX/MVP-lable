# Подключение артиста к площадкам — флоу

## Реальность API (2026)

| Площадка | Публичные метрики | Полные стримы / кабинет | Как подключаем |
|----------|-------------------|-------------------------|----------------|
| **Spotify** | followers, popularity (Web API, client credentials) | Spotify for Artists — **не** в public API (только партнёры/дистрибьютор) | OAuth popup (аккаунт) + link `artist_id` → sync followers |
| **Apple Music** | catalog artist (developer JWT) | Analytics API — **provider/label only** | link Apple Music artist id (без user OAuth на стримы) |
| **Yandex Music** | limited via user token (неофиц.) | кабинет артиста / партнёрка | OAuth Яндекс ID + link artist id |
| **VK Music** | stats сообщества | Студия / карточка артиста | OAuth VK (groups) + link `group_id` |

**Вывод:** окно входа как у Google (OAuth) — да, где API это позволяет (Spotify, Yandex, VK).  
Полные стримы по трекам через публичный OAuth **нельзя** — только partners / CSV дистрибьютора / ручной ввод. MVP: OAuth + public followers + manual/estimate royalties.

## UX флоу (фронт)

1. Кабинет → Platforms  
2. **Connect Spotify** → `GET /platforms/spotify/start` → popup `authorize_url`  
3. Callback закрывает popup, статус `connected`  
4. Артист вставляет Spotify Artist URI/ID → `POST /platforms/spotify/link-artist`  
5. **Sync** → `POST /platforms/spotify/sync` (followers/popularity)  
6. Аналогично Yandex / VK  
7. Apple: только **Link artist id** (без popup)

## Backend endpoints

```
GET  /platforms/
GET  /platforms/spotify/start | /callback
POST /platforms/spotify/link-artist | /sync
GET  /platforms/yandex/start | /callback
POST /platforms/yandex/link-artist
GET  /platforms/vk/start | /callback
POST /platforms/vk/link-artist
POST /platforms/apple/link-artist
DELETE /platforms/{platform}
```

Env: `SPOTIFY_CLIENT_ID/SECRET`, `YANDEX_*`, `VK_*`, `APPLE_TEAM_ID/KEY_ID/PRIVATE_KEY_*`, redirect URIs.

## Auto-publish

После `approved`: в `release_date` (UTC) job публикует → `published`.

```
POST /jobs/auto-publish          # Header X-Cron-Secret
POST /jobs/auto-publish/manual   # Admin
```

Cron пример: `*/15 * * * * curl -X POST -H "X-Cron-Secret: $CRON_SECRET" https://api/.../jobs/auto-publish`
