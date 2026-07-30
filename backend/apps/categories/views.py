"""
Views for the categories app.
"""
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView

from common.utils.responses import success_response
from .services import CategoryService


class CategoryTreeView(APIView):
    """GET /api/v1/categories/tree/ — full category tree (cached)."""
    permission_classes = [AllowAny]

    def get(self, request):
        return success_response(CategoryService.get_tree(), message="Category tree")
