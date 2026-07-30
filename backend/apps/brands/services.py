"""
Service layer for the brands app.
"""
from .models import Brand


class BrandService:
    @staticmethod
    def list_active():
        return Brand.objects.filter(is_active=True, is_deleted=False).order_by("name")
