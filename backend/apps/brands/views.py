from rest_framework.permissions import AllowAny
from rest_framework.generics import ListAPIView

from .serializers import BrandSerializer
from .services import BrandService


class BrandListView(ListAPIView):
    """GET /api/v1/brands/"""
    permission_classes = [AllowAny]
    serializer_class = BrandSerializer

    def get_queryset(self):
        return BrandService.list_active()
