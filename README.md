# WEBTECH — Next Generation Electronics Store

> A premium, enterprise-grade electronics e-commerce platform. Django REST Framework backend + React 19 / TypeScript / Three.js frontend, built with a strict clean-architecture discipline and verified end-to-end through live testing rather than assumption.

---

## Table of Contents

- [Overview](#overview)
- [Tech Stack](#tech-stack)
- [Architecture](#architecture)
- [Project Structure](#project-structure)
- [What's Implemented](#whats-implemented)
- [API Response Format](#api-response-format)
- [Demo Data](#demo-data)
- [Getting Started](#getting-started)
- [Testing Philosophy](#testing-philosophy)
- [Performance](#performance)
- [Git History](#git-history)
- [Roadmap](#roadmap)

---

## Overview

WEBTECH is not a template store — it's an attempt at a real, production-shaped electronics marketplace: the kind of experience you'd expect from Apple, Sony, or Nothing, backed by a Django architecture that could plausibly serve millions of products and users.

The design brief called for cinematic 3D product presentation, glassmorphism UI, and an Awwwards-caliber storefront. The engineering brief called for Clean Architecture, a fully normalized PostgreSQL schema, JWT auth with refresh rotation, and REST endpoints that never leak framework defaults into the response shape. Both sides are implemented — and both sides have been exercised against a running server, not just read back from the source.

**Live, verified capabilities include:**
- Full customer journey: register → browse → search → product detail (3D viewer) → cart → checkout → order tracking
- Guest cart that merges into the user's cart on login/register (session-key based)
- JWT access/refresh rotation with blacklist-on-rotation, tested end-to-end
- Reviews with automatic verified-purchase detection (checked against real order history, not a checkbox)
- A protected Admin Dashboard (product CRUD, order management, analytics, support-ticket handling, inventory restocking) — role-gated and confirmed to return `403` for non-admins
- A notification system wired into real events (order placed, order status changed, support ticket replied)
- An inventory audit trail: every sale automatically logs a `StockMovement` tied to the real order number

## Tech Stack

**Frontend**
React 19 · TypeScript · Vite · Tailwind CSS · Framer Motion · Three.js / React Three Fiber / Drei · React Router · TanStack Query · Axios · React Hook Form · Zod · Zustand · Recharts

**Backend**
Python · Django 5/6 · Django REST Framework · PostgreSQL · Redis · Celery · SimpleJWT · drf-spectacular (Swagger/Redoc) · Docker

**Deployment target**
Frontend → Vercel · Backend → Railway / Render / any Docker host · DB → PostgreSQL · Cache/Broker → Redis

## Architecture

```
Frontend (React 19 + TS)
        ↓
   API Gateway  (/api/v1/, DRF)
        ↓
 Authentication Layer  (JWT, rotation, blacklist)
        ↓
  Business Services Layer   ← all business logic lives here, never in Views
        ↓
     Database Layer (PostgreSQL)
        ↓
 Storage (Cloudinary) · Cache (Redis) · Background Jobs (Celery)
```

Every Django app follows the same strict layering:

```
Views  →  Serializers  →  Services  →  Models  →  Database
```

- **Views** parse the request and return a response — nothing else.
- **Serializers** handle (de)serialization and field-level validation only.
- **Services** own every business rule (stock checks, cart merges, checkout math, notification triggers, permission edge cases). This is where the actual logic lives, and it's unit-testable in isolation from HTTP.
- **Models** define table shape. A shared `common.models.BaseModel` gives every table a UUID primary key, `created_at`/`updated_at`, and soft delete.

This isn't cosmetic — it's what let features like "notify the customer when an admin changes an order status" or "merge a guest cart on login" get implemented as a one-line service call from two different call sites, instead of duplicated logic sprayed across views.

## Project Structure

```
webtech/
├── backend/
│   ├── core/
│   │   ├── settings/          # base.py, development.py, production.py
│   │   ├── urls.py            # mounts every app under /api/v1/
│   │   └── celery.py
│   ├── apps/                  # 18 apps, each: models / serializers / services / views / urls / admin
│   │   ├── authentication/    # JWT register/login/logout/refresh/password-reset
│   │   ├── users/              # custom User (email login) + profile
│   │   ├── products/           # catalog: products, variants, images, specs
│   │   ├── categories/         # category tree (self-referencing)
│   │   ├── brands/
│   │   ├── inventory/          # warehouses, stock movements, restock, audit trail
│   │   ├── cart/                # guest + user cart, session-key merge on login
│   │   ├── wishlist/
│   │   ├── orders/              # checkout: cart → order, tax, shipping, stock reduction
│   │   ├── payments/            # COD (functional) + pluggable Stripe/PayPal hook
│   │   ├── reviews/             # ratings, verified-purchase check, helpful votes
│   │   ├── addresses/
│   │   ├── coupons/             # percentage/fixed, usage limits, min purchase
│   │   ├── notifications/       # in-app notifications wired to real events
│   │   ├── analytics/           # top products, sales by category, revenue trend, customer segments
│   │   ├── dashboard/           # admin stats + product/order management API
│   │   ├── search/              # full-text search, autocomplete, recent/popular
│   │   └── support/             # ticketed support with threaded replies
│   ├── common/                  # shared BaseModel, standard responses, role permissions, email tasks
│   ├── requirements.txt / Dockerfile / docker-compose.yml
│   └── README.md                # chronological git log for the backend portion
├── frontend/
│   ├── src/
│   │   ├── components/          # layout, home, product, account, admin, ui
│   │   ├── pages/                # Home, Product, Category, Search, Cart, Checkout, Account/*, Admin/*, Support
│   │   ├── hooks/                 # one hook module per domain (useCart, useAuth, useAdmin, useSearch...)
│   │   ├── services/               # one Axios service per domain, matching backend URL-for-URL
│   │   ├── store/                   # Zustand: auth state (JWT + user)
│   │   ├── routes/                  # route-level code splitting via React.lazy
│   │   └── three/scenes/            # Hero 3D scene + interactive product viewer
│   ├── package.json
│   └── README.md                    # chronological git log for the frontend portion
├── database/
│   └── SCHEMA.md                    # full table-by-table schema reference
├── RUN.md                            # step-by-step run instructions (Docker and manual)
└── README.md                         # this file
```

## Design Update: Light Theme, Welcome Experience & New Animations

The site shipped with a cinematic dark theme per the original design brief. Based on direct feedback, it went through a real conversion pass:

- **Light theme, done properly** — not just lightened colors, a full conversion: every page background, card, border, and text color across ~30 files was systematically converted from the dark palette to a light one (`#F7F8FA` page background, white cards, `slate-*` text/borders). This caught and fixed real contrast bugs along the way — a notification dropdown that would've rendered white text on a white background, a loading spinner that would've been invisible, translucent "glass" cards that only worked against a near-black background and needed to become solid white + shadow instead. The Hero section and main navigation intentionally **stay dark** as a deliberate cinematic accent (a common premium-brand pattern — think Apple's dark hero sections on an otherwise light site).
- **Welcome / loading splash screen** — the "Landing Experience" from the original animation spec, actually built: an animated WEBTECH logo reveal with soft glow, floating particles, and a progress bar, shown once per browser session before the Hero loads.
- **New animations** — magnetic buttons (the CTA buttons subtly pull toward the cursor, per the original spec's "Magnetic Buttons" requirement that hadn't been implemented yet), and an animated stats section on the homepage with real, API-backed counters (product count, brand count) that count up when scrolled into view.

**A note on that conversion:** the first automated pass (bulk find/replace across ~30 files) technically worked but produced an undisciplined result — 6 different scattered gray text shades, 3 different border shades, and leftover `backdrop-blur` on now-solid white elements that used to be translucent dark glass. A follow-up pass fixed this properly: consolidated down to exactly two text tones (`slate-900` primary, `slate-500` muted) and one consistent border tone (`slate-200`), removed the pointless blur, and — in the process of tightening things up — caught two real contrast bugs: the wishlist/quick-view icon buttons on product cards were rendering dark text directly on a dark image overlay (invisible), and the "Out of Stock" label had the same problem.

**A more serious bug the "check everything again" request caught:** the Navbar was designed to start fully transparent at the top of every page (with white text) and only turn into a solid dark bar on scroll — which worked fine when the whole site was dark, because a transparent navbar over a dark Hero was still readable. After the light-theme conversion, every page *except* Home now has a light background, so that same transparent-white-text navbar became **invisible** the instant someone landed on `/cart`, `/login`, `/account`, or any other page at the top of the scroll. Fixed: the Navbar is now only transparent at the very top of the Home page (over the dark Hero) and solid everywhere else. While auditing this, also fixed a missing scroll-reset on route change (SPA navigation doesn't reset scroll position by default) and three places where a hover state had been accidentally consolidated to the exact same color as the resting state, making them appear unresponsive.

## Compare Products

A dedicated comparison feature — one of the original spec's requirements that had been missing. Add up to 4 products to compare from any product card or the product detail page (a `Scale` icon toggle); a floating bar appears showing the count with a "Compare Now" button. The `/compare` page renders a full side-by-side table — price, stock, warranty, and the union of every spec across the selected products (so it lines up correctly even when products don't share identical spec sets). The compare list persists in `localStorage`, so it survives a page refresh.

While wiring this in, two more contrast bugs from the light-theme conversion surfaced and got fixed: a "Sale" badge with dark text on its blue background (nearly invisible), and a "Save address" button with no explicit text color at all, silently inheriting dark text onto the same blue background.

## Design System Cleanup

Real user feedback: the light-theme pages felt inconsistent with each other. The root cause was structural — every page had its own hand-written button/badge className strings, so styles quietly drifted apart edit after edit. This got fixed at the source, not just patched:

- **One accent color.** The UI previously mixed blue, purple, and cyan decoratively across the Hero, badges, and icons with no real system behind which page got which color. Collapsed down to a single brand accent (blue) everywhere decorative; the only other colors that appear now are semantic (green = success/verified, amber = pending, red = danger) — the same convention every major design system uses, not random accents.
- **Fixed a batch of leftover dark-theme colors** (`yellow-400`, `green-400`, `red-400`) that read fine against the old near-black background but had washed-out, poor contrast against the new white one — order status badges, low-stock warnings, and form error messages across ~10 files.
- **Shared `Button` and `Badge` components**, the actual fix for the inconsistency complaint: every primary CTA (login, register, checkout, add to cart, save address...) now renders from one `Button` component with five defined variants, instead of five different pages each hand-rolling their own version of "the primary button" that could (and did) diverge.

## What's Implemented

All 18 backend apps have real, tested implementations — not scaffolding. Each one was verified by running an actual Django dev server and hitting it with `curl` through the full flow (register, add to cart, checkout, admin actions, etc.) before being considered done.

| App | What it does | Verified live |
|---|---|---|
| `authentication` | JWT register/login/logout/logout-all, refresh rotation + blacklist, password reset | ✅ full token lifecycle including rotation-blacklist rejection |
| `users` | Custom email-login `User`, profile | ✅ |
| `products` | Catalog, variants, images, specs, filtering/sorting/pagination | ✅ |
| `categories` / `brands` | Tree-structured categories, brand list, Redis-cached tree | ✅ |
| `cart` | Guest cart (session key) + user cart, **merges into the user's cart on login/register** | ✅ merge confirmed end-to-end |
| `orders` | Checkout: cart → order, VAT + flat shipping, coupon application, stock reduction | ✅ |
| `payments` | Cash-on-delivery fully functional; Stripe/PayPal wired as a pluggable gateway stub | ✅ (COD path) |
| `reviews` | Ratings + comments, **verified-purchase flag computed from real order history**, helpful votes | ✅ |
| `wishlist` | Add/remove/list, "move to cart" | ✅ |
| `addresses` | Full CRUD, single default address enforced | ✅ |
| `coupons` | Percentage/fixed discounts, expiry, usage limits, min purchase, one-per-customer | ✅ |
| `notifications` | Wired to real events: order placed, order status changed, ticket replied | ✅ notification delivery confirmed after each trigger |
| `dashboard` | Admin-only stats, product CRUD, order status management — role-gated | ✅ 403 confirmed for non-admins |
| `analytics` | Top products, sales by category, revenue trend, new-vs-returning customers | ✅ verified against seeded orders with known totals |
| `inventory` | Stock-movement audit trail auto-logged on every sale, manual restock | ✅ math verified (10 − 3 + 20 = 27) |
| `search` | Full-text search, autocomplete suggestions, recent + popular searches | ✅ |
| `support` | Ticketed support, threaded replies, auto status transition, admin management | ✅ full ticket → reply → notification loop confirmed |

**Frontend pages**: Home (3D hero + featured products), Category (filters/sort/pagination), Search (fullscreen overlay + results page), Product Detail (interactive 3D viewer, variants, reviews, related products), Cart, Checkout, Account (overview, orders, addresses, wishlist, settings), Support, and a full Admin section (overview with charts, products, orders, analytics, support).

## API Response Format

Every endpoint returns the same envelope — including endpoints that would, by DRF's defaults, return something different (this was actually a real bug that got caught and fixed: `BrandListView` originally leaked DRF's default `{count, next, previous, results}` shape before being brought in line with the rest of the API):

```json
// Success
{ "success": true, "message": "...", "data": { } }

// Error
{ "success": false, "message": "...", "errors": { } }
```

## Demo Data

Every page in this project can be populated with realistic content in one command — no more empty states or placeholder text:

```bash
python manage.py seed_demo_data
```

This creates **27 real brands** (Apple, Samsung, Sony, ASUS, Razer, NVIDIA, DJI, Meta, HP, Canon, and more) across **24 categories** — the original 12 (smartphones, laptops, gaming, monitors, keyboards, mouse, headphones, earbuds, speakers, tablets, smart watches, cameras) plus 12 more (gaming consoles, VR headsets, drones, smart home, networking, storage, graphics cards, processors, TVs, projectors, printers, streaming devices) — and **67 real products** with actual product names (iPhone 15 Pro Max, PlayStation 5, DJI Mini 4 Pro, NVIDIA GeForce RTX 4090, Meta Quest 3...), real specs, color/storage variants where relevant, 2 working coupon codes, 6 demo customer accounts with completed orders, and 50+ reviews (several genuinely verified-purchase, tied to real seeded orders).

**Images are real and category-relevant**, not random unrelated placeholders — each product's photos come from [LoremFlickr](https://loremflickr.com), a keyword-based real-photo service, so a drone product actually shows a real drone photo, a graphics card shows a real graphics card, etc. (Confirmed operational as of mid-2026, after Flickr lifted its earlier API restrictions.)

It's idempotent — safe to run again.

Verified live after seeding: Home's featured section, every one of the 24 category pages, full-text search, product detail pages (specs/variants/reviews/related products), and the Admin Dashboard's stats and analytics charts all render real, non-empty, category-appropriate data.

## Getting Started

See [`RUN.md`](./RUN.md) for full setup instructions (Docker-based and manual, including environment variables). Quick version:

```bash
# Backend
cd backend
cp .env.example .env
docker-compose up --build

# Frontend
cd frontend
cp .env.example .env
npm install
npm run dev
```

Backend: `http://localhost:8000` (Swagger at `/api/docs/`) · Frontend: `http://localhost:5173`

## Testing Philosophy

Nothing in this codebase was marked "done" without being run. The workflow for every feature was:

1. Implement models → `makemigrations` → `migrate` against a real (SQLite, for speed) database
2. Start an actual `runserver` process
3. Drive it with `curl` through the real flow — register a user, add to cart, check out, verify the response shape
4. Where a bug surfaced (and several real ones did — see the [full git log](./GIT_LOG.md) for specifics), fix it and re-run the same test before moving on

This caught issues that reading the code never would have: a login flow that silently never sent the header needed to merge a guest cart, an admin form that would always 400 because it was missing required fields, cross-user data leaking through a client-side cache that was never cleared on logout, and more. All fixed, all re-verified.

## Performance

The initial production build carried a ~1.9MB main bundle — mostly Three.js and Recharts pulled into every route. This has been fixed with route-level `React.lazy()` splitting plus explicit Vite `manualChunks` for the heavy vendor libraries:

| Bundle | Before | After |
|---|---|---|
| Main entry chunk | 1.9 MB | **155 KB** (52 KB gzipped) |
| Three.js (3D viewer) | bundled into every route | separate chunk, loads only on Home/Product pages |
| Recharts (admin charts) | bundled into every route | separate chunk, loads only on Admin pages |

## Git History

Every file in this project was created or modified with its own `git add` + `git commit -m "..."` — nothing was batch-committed. The full chronological history (500+ commits) is available in [`GIT_LOG.md`](./GIT_LOG.md), and the backend/frontend-specific portions are documented in `backend/README.md` and `frontend/README.md` respectively.

## Roadmap

Everything functionally required for a working store is implemented and tested. Remaining ideas, roughly in priority order:

- Real payment gateway integration (Stripe/PayPal) behind the existing pluggable interface
- Multi-warehouse allocation UI on top of the existing `Inventory` model
- WebSocket-based live notifications (currently 30s polling)
- E2E test suite (Playwright/Cypress) to complement the manual `curl`-driven verification this project was built with
