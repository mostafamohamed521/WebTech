"""
Views for the coupons app.
"""
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView

from common.utils.responses import success_response, error_response
from apps.cart.services import CartService
from .services import CouponService


class ValidateCouponView(APIView):
    """POST /api/v1/coupons/validate/  { "code": "SAVE10" } — validates against the caller's current cart subtotal."""
    permission_classes = [IsAuthenticated]

    def post(self, request):
        code = request.data.get("code")
        if not code:
            return error_response({"code": ["This field is required."]}, message="Invalid input")
        cart = CartService.get_or_create_cart(request.user)
        subtotal = CartService.subtotal(cart)
        coupon = CouponService.validate_and_get(code, request.user, subtotal)
        discount = coupon.calculate_discount(subtotal)
        return success_response(
            {"code": coupon.code, "discount": str(discount), "subtotal": str(subtotal)},
            message="Coupon is valid",
        )
