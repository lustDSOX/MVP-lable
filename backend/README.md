# Backend — Label Management API

FastAPI + PostgreSQL + JWT. Версия API: **0.0.3**

## Быстрый старт

```bash
cd backend
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
docker compose -f db/docker-compose.yml up -d
# поправь POSTGRES_* в .env
uvicorn main:app --reload --port 8000
```

Swagger: http://localhost:8000/docs

## Эндпоинты

| Группа | Путь | Кто |
|--------|------|-----|
| Auth | `POST /users/register`, `POST /users/login` | public |
| Profile | `GET/PATCH /users/profile*` | auth |
| Admin role | `PATCH /admin/users/{id}/role` | admin |
| Releases | CRUD + submit | owner |
| Status | `PATCH /releases/{id}/status` | mod/admin |
| Queue | `GET /moderation/queue` | mod/admin |
| Tracks | `/releases/{id}/tracks`, `/tracks/{id}` | owner |
| Links | `/releases/{id}/links` | owner/staff |
| Public | `GET /releases/`, `GET /releases/search` | public |

Файлы (S3) и Spotify — пока нет; `master_file` / `preview_file` — строковые заглушки.
