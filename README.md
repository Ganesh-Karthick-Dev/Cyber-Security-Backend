### CyberGuide Micro-SaaS Platform

Backend: FastAPI (Python), PostgreSQL, Redis. Frontend: Next.js. Kali tools in a separate container.

Quick start:
- Copy backend/.env.example to backend/.env and set SECRET_KEY and DATABASE_URL
- From docker/: run `docker compose build` then `docker compose up`
- Backend: http://localhost:8000 (docs at /docs). Nginx at http://localhost/

Environment variables (backend/.env):
- SECRET_KEY, DATABASE_URL, STRIPE_SECRET_KEY, STRIPE_PUBLISHABLE_KEY, REDIS_URL

API highlights:
- Auth: /api/v1/auth/register, /login, /me, /refresh
- Sites: /api/v1/sites
- Scans: /api/v1/scans/start, /start/{scan_type}, /{scan_id}/status, /{site_id}/latest, /{site_id}/history
- AI: /api/v1/ai/*
- Billing: /api/v1/plans, /api/v1/subscriptions/*

Notes:
- Tables autoload on startup; use Alembic for production migrations.
- Kali scan currently performs minimal safe calls; tune flags with care.



