from django.apps import AppConfig


class CouponsConfig(AppConfig):
    """Configuration for the coupons app.

    Purpose: Discount coupons, usage limits, validation rules.
    """
    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.coupons"
    verbose_name = "Coupons"
