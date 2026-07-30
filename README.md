# WEBTECH — Next Generation Electronics Store

منصة إلكترونيات إنتربرايز فاخرة (Apple × Tesla × Nothing × Sony × Samsung × Razer × ASUS ROG) بهوية بصرية مستقلة، تجربة تسوق سينمائية بـ 3D وanimations فاخرة، وبنية Backend/Frontend/Database على مستوى إنتاج حقيقي.

## نظرة عامة على المشروع

WEBTECH مش متجر إلكتروني تقليدي — الهدف إن كل صفحة تحكي قصة، وكل تمرير (scroll) يكشف عن حاجة جديدة، وكل تفاعل حسه فاخر. المنصة مبنية عشان تخدم ملايين المستخدمين والمنتجات بأداء عالي وأمان كامل.

## البنية المعمارية (Architecture)

```
Frontend (React 19 + TS)
        ↓
   API Gateway (/api/v1/)
        ↓
 Authentication Layer (JWT)
        ↓
  Business Services Layer   ← كل منطق العمل هنا، مش في الـ Views
        ↓
     Database Layer (PostgreSQL)
        ↓
   Storage (Cloudinary) + Cache (Redis) + Background Jobs (Celery)
```

## الـ Tech Stack

**Frontend:** React 19, TypeScript, Vite, TailwindCSS, Shadcn UI, Framer Motion, GSAP, Three.js, React Three Fiber, React Router, TanStack Query, Axios, React Hook Form, Zod, Zustand

**Backend:** Python, Django 5, Django REST Framework, PostgreSQL, Redis, Celery, Docker, Swagger (drf-spectacular), Cloudinary

**Deployment:** Frontend → Vercel · Backend → Railway/Render/VPS · DB → PostgreSQL · Cache → Redis

## هيكل المشروع (Project Structure)

```
webtech/
├── backend/
│   ├── core/                  # settings, urls, wsgi/asgi, celery
│   │   └── settings/          # base.py, development.py, production.py
│   ├── apps/                  # كل تطبيق مستقل: models/serializers/services/views/urls/admin/tests
│   │   ├── authentication/
│   │   ├── users/
│   │   ├── products/
│   │   ├── categories/
│   │   ├── brands/
│   │   ├── inventory/
│   │   ├── cart/
│   │   ├── wishlist/
│   │   ├── orders/
│   │   ├── payments/
│   │   ├── reviews/
│   │   ├── addresses/
│   │   ├── coupons/
│   │   ├── notifications/
│   │   ├── analytics/
│   │   ├── dashboard/
│   │   ├── search/
│   │   └── support/
│   ├── common/                 # utils, permissions, emails, logs (مشترك بين كل الـ apps)
│   ├── requirements.txt
│   ├── Dockerfile
│   ├── docker-compose.yml
│   └── README.md               # سجل عمليات git الخاصة بالباك اند
├── frontend/
│   ├── src/
│   │   ├── components/         # layout, home, product, cart, ui...
│   │   ├── pages/               # Home, Product, Cart, Checkout, Account...
│   │   ├── hooks/
│   │   ├── services/            # apiClient (axios)
│   │   ├── store/                # zustand (auth, cart)
│   │   ├── routes/
│   │   ├── types/
│   │   └── three/                # مشاهد الـ 3D
│   ├── package.json
│   └── README.md               # سجل عمليات git الخاصة بالفرونت اند
├── database/
│   └── SCHEMA.md                # مخطط قاعدة البيانات الكامل (كل الجداول)
├── README.md                    # الملف ده — وصف المشروع الكامل
└── RUN.md                       # طريقة تشغيل المشروع خطوة بخطوة
```

## معمارية الباك اند (Clean Architecture)

كل تطبيق (app) في `backend/apps/` بيتبع نفس الطبقات، والقاعدة الأساسية: **منطق العمل (Business Logic) ميعيشش أبدًا جوه الـ Views**.

```
Views  →  Serializers  →  Services  →  Models  →  Database
```

- **Views**: تستقبل الـ request وترجع response بس (باستخدام صيغة الاستجابة الموحدة في `common/utils/responses.py`)
- **Serializers**: تحويل وتحقق على مستوى الحقول (field-level validation)
- **Services**: هنا كل قواعد العمل (business rules) الحقيقية
- **Models**: شكل الجداول بس

## صيغة استجابة الـ API الموحدة

```json
// نجاح
{ "success": true, "message": "...", "data": {} }

// خطأ
{ "success": false, "message": "...", "errors": {} }
```

## الوحدات الأساسية (System Modules)

Authentication · Users · Products · Categories · Brands · Inventory · Cart · Wishlist · Checkout · Orders · Payments · Reviews · Coupons · Notifications · Search · Analytics · Dashboard · Support · Settings

## الحالة الحالية للمشروع

**تحديث 3:** صفحة المنتج الكاملة شغالة فعليًا مع نظام تقييمات ومفضلة حقيقيين:

- **Backend (تطبيقين جديدين، مُختبرين حي):**
  - `reviews`: تقييم بالنجوم + تعليق، **verified purchase** بيتحقق تلقائيًا من `OrderItem` الحقيقي، تجميع متوسط التقييم وتوزيع النجوم (1-5)، helpful votes قابلة للتبديل (toggle). اتعمله اختبار حي: نشر review فعلي، وشوفت الـ summary (average 5.0) راجع صح.
  - `wishlist`: إضافة/حذف/عرض، مربوط بمنتجات حقيقية.

- **Frontend — صفحة المنتج كاملة (`/product/:slug`):**
  - **3D Viewer تفاعلي حقيقي** بـ OrbitControls: drag لتدوير المنتج، scroll للزووم، auto-rotate وقت الخمول، ولون الموديل بيتغير حسب الـ variant المختار
  - اختيار الفاريانت (لون/سعة/رام) وتحديث السعر تلقائيًا
  - إضافة للسلة والمفضلة، جدول المواصفات الكامل
  - قسم تقييمات كامل: ملخص بصري لتوزيع النجوم، فورم كتابة تقييم (للمسجلين بس)، وزر "helpful" تفاعلي
  - منتجات مشابهة (related products) من نفس التصنيف

- **باقي الـ 7 تطبيقات** (`notifications`, `analytics`, `dashboard`, `search`, `support`, `inventory`) لسه على شكل الهيكل الأساسي.
- **باقي صفحات الفرونت اند** (Category, Account Dashboard, Compare, Admin panel) لسه هيكل فاضي.

كل ملف اتعمل أو اتعدل، اتعمله `git add` + `git commit -m "..."` منفصل، زي ما هو موضح في `backend/README.md` و `frontend/README.md`.

## للتشغيل

راجع ملف [`RUN.md`](./RUN.md) لخطوات التشغيل الكاملة (باك اند + فرونت اند + قاعدة البيانات).
