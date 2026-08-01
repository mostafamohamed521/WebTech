"""
Service layer for the coupons app: validation + discount calculation.
"""
from django.utils import timezone
from rest_framework.exceptions import ValidationError

from .models import Coupon, CouponUsage


class CouponService:
    @staticmethod
    def validate_and_get(code: str, user, subtotal) -> Coupon:
        try:
            coupon = Coupon.objects.get(code__iexact=code, is_active=True, is_deleted=False)
        except Coupon.DoesNotExist:
            raise ValidationError({"coupon": ["Invalid or inactive coupon code."]})

        if coupon.expiration and coupon.expiration < timezone.now():
            raise ValidationError({"coupon": ["This coupon has expired."]})

        if subtotal < coupon.min_purchase:
            raise ValidationError({"coupon": [f"Minimum purchase of {coupon.min_purchase} required."]})

        if coupon.usage_limit is not None:
            used = CouponUsage.objects.filter(coupon=coupon).count()
            if used >= coupon.usage_limit:
                raise ValidationError({"coupon": ["This coupon has reached its usage limit."]})

        already_used = CouponUsage.objects.filter(coupon=coupon, user=user).exists()
        if already_used:
            raise ValidationError({"coupon": ["You have already used this coupon."]})

        return coupon

    @staticmethod
    def record_usage(coupon: Coupon, user, order=None):
        CouponUsage.objects.create(coupon=coupon, user=user, order=order)
