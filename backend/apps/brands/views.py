from rest_framework.permissions import AllowAny
from rest_framework.views import APIView

from common.utils.responses import success_response
from .serializers import BrandSerializer
from .services import BrandService


class BrandListView(APIView):
    """GET /api/v1/brands/"""
    permission_classes = [AllowAny]

    def get(self, request):
        brands = BrandService.list_active()
        return success_response(BrandSerializer(brands, many=True).data, message="Brands")
