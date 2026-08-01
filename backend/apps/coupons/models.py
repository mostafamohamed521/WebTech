"""
Models for the coupons app.
"""
from django.db import models
from common.models import BaseModel
from apps.users.models import User


class Coupon(BaseModel):
    class DiscountType(models.TextChoices):
        PERCENTAGE = "percentage", "Percentage"
        FIXED = "fixed", "Fixed Amount"

    code = models.CharField(max_length=40, unique=True, db_index=True)
    type = models.CharField(max_length=12, choices=DiscountType.choices, default=DiscountType.PERCENTAGE)
    value = models.DecimalField(max_digits=10, decimal_places=2)
    expiration = models.DateTimeField(null=True, blank=True)
    usage_limit = models.PositiveIntegerField(null=True, blank=True)
    min_purchase = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    is_active = models.BooleanField(default=True)

    class Meta:
        db_table = "coupons"
        indexes = [models.Index(fields=["code"])]

    def __str__(self):
        return self.code

    def calculate_discount(self, subtotal):
        if self.type == self.DiscountType.PERCENTAGE:
            return (subtotal * self.value) / 100
        return min(self.value, subtotal)


class CouponUsage(BaseModel):
    coupon = models.ForeignKey(Coupon, on_delete=models.CASCADE, related_name="usages")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="coupon_usages")
    order = models.ForeignKey("orders.Order", on_delete=models.SET_NULL, null=True, blank=True)

    class Meta:
        db_table = "coupon_usage"
