"""
Service layer for the categories app.
"""
from django.core.cache import cache
from .models import Category


class CategoryService:
    CACHE_KEY = "categories:tree"
    CACHE_TTL = 60 * 15

    @staticmethod
    def get_tree():
        tree = cache.get(CategoryService.CACHE_KEY)
        if tree is not None:
            return tree
        roots = Category.objects.filter(parent__isnull=True, is_active=True, is_deleted=False).order_by("sort_order")
        from .serializers import CategoryTreeSerializer
        tree = CategoryTreeSerializer(roots, many=True).data
        cache.set(CategoryService.CACHE_KEY, tree, CategoryService.CACHE_TTL)
        return tree
