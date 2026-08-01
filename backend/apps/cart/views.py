"""
Views for the cart app. Works for both guests (session_key from
X-Session-Key header) and authenticated users (JWT).
"""
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView

from common.utils.responses import success_response, error_response
from .serializers import CartSerializer, AddCartItemSerializer, UpdateCartItemSerializer
from .services import CartService


def _resolve_cart(request):
    user = request.user if request.user.is_authenticated else None
    session_key = request.headers.get("X-Session-Key")
    return CartService.get_or_create_cart(user=user, session_key=session_key)


class CartView(APIView):
    """GET /api/v1/cart/"""
    permission_classes = [AllowAny]

    def get(self, request):
        cart = _resolve_cart(request)
        return success_response(CartSerializer(cart).data, message="Cart")


class CartItemView(APIView):
    """POST /api/v1/cart/items/ — add item."""
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = AddCartItemSerializer(data=request.data)
        if not serializer.is_valid():
            return error_response(serializer.errors, message="Invalid item")
        cart = _resolve_cart(request)
        CartService.add_item(cart, **serializer.validated_data)
        return success_response(CartSerializer(cart).data, message="Item added to cart", status=201)


class CartItemDetailView(APIView):
    """PATCH/DELETE /api/v1/cart/items/<id>/"""
    permission_classes = [AllowAny]

    def patch(self, request, item_id):
        serializer = UpdateCartItemSerializer(data=request.data)
        if not serializer.is_valid():
            return error_response(serializer.errors, message="Invalid quantity")
        cart = _resolve_cart(request)
        CartService.update_item(cart, item_id, serializer.validated_data["quantity"])
        return success_response(CartSerializer(cart).data, message="Cart item updated")

    def delete(self, request, item_id):
        cart = _resolve_cart(request)
        CartService.remove_item(cart, item_id)
        return success_response(CartSerializer(cart).data, message="Item removed")


class ClearCartView(APIView):
    """DELETE /api/v1/cart/clear/"""
    permission_classes = [AllowAny]

    def delete(self, request):
        cart = _resolve_cart(request)
        CartService.clear(cart)
        return success_response(message="Cart cleared")
