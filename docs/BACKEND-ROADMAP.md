# Backend Roadmap — CLASS TICKETS / MVP-lable

Статус на 2026-08-18.  
Стек: **FastAPI · SQLAlchemy async · PostgreSQL · Alembic · JWT · passlib/bcrypt**  
Код: `backend/` · фронт пока на mock, API не подключён.

Цель: MVP лейбла — роли, релизный пайплайн, файлы, модерация, статистика, документы.

См. также **[RELEASE-AND-CONTRACT.md](./RELEASE-AND-CONTRACT.md)** (форма релиза / 1 договор на релиз).

---

## 0. Уже есть (as-is)

- FastAPI, `/health`, Swagger
- JWT register/login, profile
- Releases CRUD + statuses draft→pending→approved/rejected→published
- RBAC ModeratorDep / AdminDep
- Tracks / links / moderation queue API (каркас)
- Models: Track, TrackContributor, ReleaseLink, TrackStat, ModerationLog

---

## Спринты (кратко)

- **B0** фундамент: requirements, RBAC, CORS — частично сделано
- **B1** Tracks & Files (S3)
- **B2** Moderation logs complete
- **B3** Links & publish
- **B4** Stats
- **B5** Documents / Contract PDF per **release**
- **B6** CMS
- **B7** Front integration

---

## Модель релиза и договора (фронт + бэк)

См. **[RELEASE-AND-CONTRACT.md](./RELEASE-AND-CONTRACT.md)**.

- 1 договор на **релиз**, не на трек
- Профиль артиста не дублировать в форме релиза
- `Track` + `TrackContributor` на каждый трек альбома/EP
- Contract: `release_id`, status signed, `file_url`

---

## Локальный запуск

```bash
cd backend
cp .env.example .env
docker compose -f db/docker-compose.yml up -d
pip install -r requirements.txt
uvicorn main:app --reload --port 8000
```
