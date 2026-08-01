"""
Service layer for the search app: live search, autocomplete
suggestions, recent + popular searches. Records every search into
SearchHistory for the popularity ranking and per-user recent list.
"""
from django.db.models import Q, Count
from django.utils import timezone
from datetime import timedelta

from apps.products.models import Product
from apps.categories.models import Category
from apps.brands.models import Brand
from .models import SearchHistory


class SearchService:
    MAX_SUGGESTIONS = 8
    RECENT_LIMIT = 10
    POPULAR_LIMIT = 8
    POPULAR_WINDOW_DAYS = 30

    @staticmethod
    def search_products(keyword: str, user=None, session_key: str | None = None):
        qs = Product.objects.filter(
            Q(name__icontains=keyword) | Q(sku__icontains=keyword) | Q(description__icontains=keyword)
            | Q(brand__name__icontains=keyword) | Q(category__name__icontains=keyword),
            published=True, is_deleted=False,
        ).select_related("brand", "category").prefetch_related("images").distinct()

        count = qs.count()
        SearchHistory.objects.create(
            user=user if user and user.is_authenticated else None,
            session_key=session_key or "",
            keyword=keyword,
            results_count=count,
        )
        return qs

    @staticmethod
    def suggestions(keyword: str):
        results = []
        for p in Product.objects.filter(name__icontains=keyword, published=True, is_deleted=False)[:SearchService.MAX_SUGGESTIONS]:
            results.append({"type": "product", "label": p.name, "slug": p.slug})
        for c in Category.objects.filter(name__icontains=keyword, is_active=True)[:3]:
            results.append({"type": "category", "label": c.name, "slug": c.slug})
        for b in Brand.objects.filter(name__icontains=keyword, is_active=True)[:3]:
            results.append({"type": "brand", "label": b.name, "slug": b.slug})
        return results[:SearchService.MAX_SUGGESTIONS]

    @staticmethod
    def recent_searches(user=None, session_key: str | None = None):
        qs = SearchHistory.objects.all()
        if user and user.is_authenticated:
            qs = qs.filter(user=user)
        elif session_key:
            qs = qs.filter(session_key=session_key, user__isnull=True)
        else:
            return []
        keywords = list(qs.order_by("-created_at").values_list("keyword", flat=True)[:SearchService.RECENT_LIMIT * 3])
        seen, unique = set(), []
        for kw in keywords:
            if kw.lower() not in seen:
                seen.add(kw.lower())
                unique.append(kw)
            if len(unique) >= SearchService.RECENT_LIMIT:
                break
        return unique

    @staticmethod
    def popular_searches():
        since = timezone.now() - timedelta(days=SearchService.POPULAR_WINDOW_DAYS)
        rows = (
            SearchHistory.objects.filter(created_at__gte=since)
            .values("keyword")
            .annotate(count=Count("id"))
            .order_by("-count")[:SearchService.POPULAR_LIMIT]
        )
        return list(rows)
