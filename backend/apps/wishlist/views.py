"""
Views for the wishlist app.
"""
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView

from common.utils.responses import success_response, error_response
from .serializers import WishlistItemSerializer
from .services import WishlistService


class WishlistView(APIView):
    """GET /api/v1/wishlist/  |  POST /api/v1/wishlist/ { "product_id": "..." }"""
    permission_classes = [IsAuthenticated]

    def get(self, request):
        items = WishlistService.list_items(request.user)
        return success_response(WishlistItemSerializer(items, many=True).data, message="Wishlist")

    def post(self, request):
        product_id = request.data.get("product_id")
        if not product_id:
            return error_response({"product_id": ["This field is required."]}, message="Invalid input")
        WishlistService.add(request.user, product_id)
        items = WishlistService.list_items(request.user)
        return success_response(WishlistItemSerializer(items, many=True).data, message="Added to wishlist", status=201)


class WishlistItemDetailView(APIView):
    """DELETE /api/v1/wishlist/<product_id>/"""
    permission_classes = [IsAuthenticated]

    def delete(self, request, product_id):
        WishlistService.remove(request.user, product_id)
        return success_response(message="Removed from wishlist")
