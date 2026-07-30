"""
Service layer for the products app.

Filtering / sorting / search business rules live here so views and
serializers stay thin.
"""
from django.db.models import Q
from .models import Product


class ProductService:
    ORDERING_MAP = {
        "newest": "-created_at",
        "oldest": "created_at",
        "price_low": "price",
        "price_high": "-price",
        "name": "name",
    }

    @staticmethod
    def base_queryset():
        return (
            Product.objects.filter(published=True, is_deleted=False)
            .select_related("brand", "category")
            .prefetch_related("images", "variants", "specifications__specification")
        )

    @staticmethod
    def list_products(*, category=None, brand=None, search=None, min_price=None,
                       max_price=None, featured=None, trending=None, ordering=None):
        qs = ProductService.base_queryset()

        if category:
            qs = qs.filter(category__slug=category)
        if brand:
            qs = qs.filter(brand__slug=brand)
        if search:
            qs = qs.filter(Q(name__icontains=search) | Q(sku__icontains=search) | Q(description__icontains=search))
        if min_price is not None:
            qs = qs.filter(price__gte=min_price)
        if max_price is not None:
            qs = qs.filter(price__lte=max_price)
        if featured is not None:
            qs = qs.filter(featured=featured)
        if trending is not None:
            qs = qs.filter(trending=trending)

        order_field = ProductService.ORDERING_MAP.get(ordering, "-created_at")
        return qs.order_by(order_field)

    @staticmethod
    def get_by_slug(slug: str) -> Product:
        return ProductService.base_queryset().get(slug=slug)

    @staticmethod
    def related_products(product: Product, limit: int = 8):
        return (
            ProductService.base_queryset()
            .filter(category=product.category)
            .exclude(id=product.id)[:limit]
        )
