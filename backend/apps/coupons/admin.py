from django.contrib import admin
from .models import Coupon, CouponUsage


@admin.register(Coupon)
class CouponAdmin(admin.ModelAdmin):
    list_display = ("code", "type", "value", "usage_limit", "expiration", "is_active")
    search_fields = ("code",)


@admin.register(CouponUsage)
class CouponUsageAdmin(admin.ModelAdmin):
    list_display = ("coupon", "user", "order", "created_at")
