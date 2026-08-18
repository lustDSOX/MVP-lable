# Backend Roadmap — CLASS TICKETS / MVP-lable

Статус на 2026-08-18.  
Стек: **FastAPI · SQLAlchemy async · PostgreSQL · Alembic · JWT (python-jose/PyJWT) · passlib/bcrypt**  
Код: `backend/` · фронт пока на mock/local state, API не подключён.

Цель бэка: довести до **рабочего MVP лейбла** — роли, релизный пайплайн, файлы, модерация, статистика с площадок, юридические документы.

---

## 0. Что уже есть (as-is)

### Инфра
| Компонент | Статус |
|-----------|--------|
| FastAPI app (`main.py`), `/health`, Swagger `/docs` | ✅ |
| CORS `allow_origins=["*"]` | ⚠️ только для dev |
| Postgres 15 + `docker-compose` | ✅ |
| Alembic migrations (users, releases, tracks, …) | ✅ |
| `requirements.txt` / Dockerfile / CI backend | ❌ |
| `.env` схема (SECRET_KEY, ALGORITHM, DB URL) | ⚠️ частично |

### Auth & Users
| Функция | Эндпоинт / место | Статус |
|---------|------------------|--------|
| Регистрация | `POST /users/register` | ✅ |
| Логин → JWT | `POST /users/login` | ✅ |
| Профиль | `GET /users/profile` | ✅ |
| Смена email / artist_name / password | `PATCH /users/profile/*` | ✅ |
| Поиск артистов | `GET /users/search` | ✅ |
| Роли в модели: `artist` / `moderator` / `admin` | enum `UserRole` | ✅ модель |
| **Проверка роли** на эндпоинтах (RBAC) | Depends | ❌ |
| Refresh token / logout / revoke | — | ❌ |
| Email verify / reset password | — | ❌ |

### Releases (ядро)
| Функция | Эндпоинт | Статус |
|---------|----------|--------|
| Создать релиз | `POST /releases/` | ✅ |
| Получить / search | `GET /releases/{id}`, `GET /releases/search` | ✅ |
| Обновить / удалить | `PATCH`, `DELETE` | ✅ |
| Submit на модерацию | `POST /releases/{id}/submit` | ✅ |
| Смена статуса (mod) | `PATCH /releases/{id}/status` | ✅ |
| Список по статусу / draft | `GET …/status/…`, `…/draft` | ✅ |
| Статусы: `draft → pending → approved/rejected → published` | enum | ✅ |

### Модели без полноценного API
| Модель | Manager | Router API | Назначение |
|--------|---------|------------|------------|
| `Track` | ✅ | ❌ | треклист релиза, master/preview paths |
| `TrackContributor` | ✅ | ❌ | соавторы / роли на треке |
| `ReleaseLink` | ✅ | ❌ | ссылки Spotify/Apple/… |
| `TrackStat` | ✅ | ❌ | стримы по дням/площадкам |
| `ModerationLog` | ✅ | ❌ | аудит решений модератора |

### Чего нет совсем
- Загрузка файлов (audio, cover, PDF контрактов)
- Интеграции Spotify / Apple Music / Yandex / VK Music
- CMS: News, Events, Guides, Cases
- Договоры / e-sign / выдача документов
- Платежи / purchase access
- Уведомления (email/Telegram)
- Подключение фронта к API (axios/fetch + auth store)

---

## 1. Общий функционал, который **должен** быть у MVP лейбла

### 1.1 Роли и доступ
- **Artist** — черновики релизов, треки, отправка на модерацию, просмотр своей статистики, подписание контракта.
- **Moderator** — очередь `pending`, approve/reject + комментарий в `ModerationLog`, превью файлов.
- **Admin** — пользователи, роли, глобальные настройки, публикация на площадки (или ручной mark `published`).

### 1.2 Релизный пайплайн
1. Artist создаёт **Release** (метаданные: title, type, UPC/ISRC later, cover).
2. Добавляет **Tracks** + upload master/preview + lyrics + explicit + contributors.
3. `submit` → `pending`.
4. Moderator review → `approved` / `rejected` (+ log).
5. После approve: генерация/подпись **договора**, затем `published` + **ReleaseLink** на площадки.
6. Фоновый/cron сбор **TrackStat** с API площадок.

### 1.3 Файлы
- Cover, audio master, audio preview, contract PDF.
- Хранение: S3-compatible (Yandex Object Storage / MinIO dev).
- Отдача: presigned URL, не публичные ключи в API.

### 1.4 Статистика
- По треку/релизу: streams per platform per day.
- Агрегаты для Dashboard артиста и отчётов модератора.
- Источники: Spotify for Artists API / Chartmetric / ручной CSV import (fallback).

### 1.5 Документы
- Шаблон договора лейбл↔артист.
- Статус: draft → sent → signed.
- MVP: PDF + отметка «подписано» + hash/timestamp; later: SimpleSign/Контур/DocuSign.

### 1.6 Публичный контент (CMS light)
- News, Events, Guides — CRUD для admin/moderator; public GET для фронта.
- Cases — каталог кейсов (сейчас только static на фронте).

### 1.7 Интеграция с фронтом
- `VITE_API_BASE_URL`, единый API client, JWT в memory/httpOnly cookie.
- Login/Register → real API; cabinets → real data; убрать mock lists.

---

## 2. Технический долг текущего кода (сразу)

| # | Проблема | Действие |
|---|----------|----------|
| 1 | Нет `requirements.txt` / lock | Зафиксировать зависимости |
| 2 | Импорты `from database import Base` vs `from db.database` | Унифицировать package layout |
| 3 | `oauth2_scheme tokenUrl="login"` не совпадает с `/users/login` | Починить OpenAPI login |
| 4 | Роль задаётся при register клиентом | Только `artist` при self-register; role меняет admin |
| 5 | Нет `require_role(...)` dependency | Добавить RBAC |
| 6 | CORS `*` | Whitelist Pages + localhost |
| 7 | Нет тестов | pytest + httpx AsyncClient |
| 8 | Файловые поля Track — строки без upload flow | S3 + endpoints |

---

## 3. Спринты бэка

### Sprint B0 — фундамент (3–5 дней) 🔴
1. `requirements.txt` + `.env.example` + README backend.
2. Починить package imports, Alembic из корня `backend`.
3. RBAC: `require_roles(UserRole.MODERATOR, UserRole.ADMIN)`.
4. Self-register только `artist`; admin endpoint смены роли.
5. CORS whitelist.
6. Dockerfile + compose: `api` + `db`.
7. Минимальные тесты: register → login → profile.

### Sprint B1 — Tracks & Files (5–7 дней) 🔴
1. Router `/releases/{id}/tracks` CRUD.
2. Contributors attach/detach.
3. Upload endpoints → S3 (MinIO в dev).
4. Валидация MIME/size (wav/flac/mp3, cover jpg/png/webp).
5. Presigned GET для preview.

### Sprint B2 — Moderation complete (3–5 дней) 🔴
1. `ModerationLog` писать при каждом status change.
2. Очередь: `GET /moderation/queue?status=pending`.
3. Reject с обязательным `reason`.
4. Права: submit только owner; status change только mod/admin.

### Sprint B3 — Links & Publish (2–4 дня) 🟡
1. CRUD `ReleaseLink` (platform + url).
2. Переход `approved → published` только admin/mod + хотя бы 1 link.
3. Public catalog: `GET /releases?status=published` для фронта Cases/Home.

### Sprint B4 — Stats (5–8 дней) 🟡
1. API `GET /tracks/{id}/stats`, `GET /releases/{id}/stats/summary`.
2. Job/script import CSV → `TrackStat`.
3. (Later) Spotify API adapter.
4. Dashboard endpoints под фронт-кабинеты.

### Sprint B5 — Documents (5–7 дней) 🟡
1. Модель `Contract` (user_id, release_id?, status, file_url, signed_at).
2. Генерация PDF из шаблона (WeasyPrint / reportlab).
3. Эндпоинты: create, get, mark signed (MVP без провайдера e-sign).
4. Хук: approved release → предложить контракт.

### Sprint B6 — CMS public (3–5 дней) 🟢
1. Models + CRUD: News, Event, Guide.
2. Public list/detail без auth.
3. Write: moderator/admin only.
4. Подключить фронт `/news`, `/events`, `/guides`.

### Sprint B7 — Front integration & harden (ongoing) 🔴→🟢
1. API client на фронте, auth store, error handling.
2. Rate limit (slowapi), request id logging.
3. Refresh tokens или short-lived access + secure cookie.
4. Deploy API (Railway/Fly/VPS) + prod DB + migrations on start.

---

## 4. Рекомендуемая карта эндпоинтов (целевая)

```
Auth/Users
  POST   /users/register
  POST   /users/login
  POST   /users/refresh          (new)
  GET    /users/profile
  PATCH  /users/profile/*
  GET    /users/search
  PATCH  /admin/users/{id}/role  (new)

Releases
  GET    /releases                 (public published)
  GET    /releases/{id}
  POST   /releases
  PATCH  /releases/{id}
  DELETE /releases/{id}
  POST   /releases/{id}/submit
  PATCH  /releases/{id}/status     (mod)
  GET    /moderation/queue         (mod)

Tracks
  GET/POST   /releases/{id}/tracks
  PATCH/DELETE /tracks/{id}
  POST       /tracks/{id}/contributors

Files
  POST /files/upload              (presign or multipart)
  GET  /files/{key}/url

Links
  GET/POST /releases/{id}/links
  DELETE   /links/{id}

Stats
  GET /tracks/{id}/stats
  GET /releases/{id}/stats/summary
  POST /stats/import               (admin)

Contracts
  GET/POST /contracts
  POST /contracts/{id}/sign

CMS
  GET/POST /news, /events, /guides
  GET      /news/{id}, …
```

---

## 5. Definition of Done — Backend MVP

- [ ] Artist регистрируется, логинится, создаёт релиз + треки + файлы, submit
- [ ] Moderator видит очередь, approve/reject с логом
- [ ] Admin назначает роли, публикует, видит пользователей
- [ ] Published релизы доступны публичным API
- [ ] Статистика хотя бы через CSV import
- [ ] Контракт: PDF + статус signed
- [ ] Фронт cabinets/login работают против реального API
- [ ] Compose: db + api + minio поднимаются одной командой
- [ ] Миграции применяются; `/health` зелёный в prod

---

## 6. Порядок относительно фронта

| Сейчас | Дальше |
|--------|--------|
| Фронт UI/mobile почти готов | Сжатие ассетов (остаток front) |
| Бэк — каркас users/releases | **B0 → B1 → B2** обязательны |
| | B3–B4 для витрины и кабинетов |
| | B5–B6 для «настоящего» лейбла |
| | B7 параллельно с деплоем |

---

## 7. Локальный запуск (когда B0 готов)

```bash
cd backend
cp .env.example .env
docker compose -f db/docker-compose.yml up -d
# after B0: docker compose up api
alembic upgrade head
uvicorn main:app --reload --port 8000
# docs: http://localhost:8000/docs
```
