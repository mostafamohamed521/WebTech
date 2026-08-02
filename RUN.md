# WEBTECH — How to Run

## Prerequisites

- Python 3.13+
- Node.js 20+
- PostgreSQL 16+
- Redis 7+
- Docker + Docker Compose (optional, but recommended)

---

## Option 1: Run with Docker (easiest)

```bash
cd backend
cp .env.example .env
docker-compose up --build
```

This automatically starts: the Django backend on `:8000`, PostgreSQL on `:5432`, Redis on `:6379`, and the Celery worker + beat.

Then, in a second terminal, start the frontend:

```bash
cd frontend
cp .env.example .env
npm install
npm run dev
```

The frontend runs on `http://localhost:5173`, the backend on `http://localhost:8000`.

---

## Option 2: Run manually (no Docker)

### Backend

```bash
cd backend
python -m venv venv
source venv/bin/activate        # on Windows: venv\Scripts\activate
pip install -r requirements.txt

cp .env.example .env
# edit .env with your real values (Postgres, Redis, Cloudinary credentials)

# make sure PostgreSQL and Redis are running locally first
python manage.py migrate
python manage.py createsuperuser
python manage.py seed_demo_data     # populates realistic demo products/brands/categories/reviews
python manage.py runserver
```

The backend runs on `http://localhost:8000`
- Swagger docs: `http://localhost:8000/api/docs/`
- Admin panel: `http://localhost:8000/admin/`

### Seeding demo data

`seed_demo_data` populates the store with realistic content so every page has something real to show instead of an empty state: 15 brands, 12 categories, 31 products (with specs, variants, and multiple images each), 2 coupon codes, 4 demo customers, and ~20 reviews (some verified against real seeded orders). It's idempotent — safe to run more than once.

```bash
python manage.py seed_demo_data          # seed (safe to re-run)
python manage.py seed_demo_data --flush  # wipe existing demo products/categories/brands first, then reseed
```

To run background tasks (optional):

```bash
celery -A core worker -l info
celery -A core beat -l info
```

### Frontend

```bash
cd frontend
cp .env.example .env
npm install
npm run dev
```

The frontend runs on `http://localhost:5173`

---

## Running Tests (Backend)

```bash
cd backend
pytest
```

## Production Build

```bash
# Backend
cd backend
python manage.py collectstatic --noinput
DJANGO_SETTINGS_MODULE=core.settings.production gunicorn core.wsgi:application

# Frontend
cd frontend
npm run build   # output in frontend/dist — ready to deploy to Vercel
```

## Important Environment Variables

See `backend/.env.example` and `frontend/.env.example` for the full list of required variables (SECRET_KEY, database credentials, Redis, Cloudinary, the frontend's API base URL).
