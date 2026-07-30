from django.apps import AppConfig


class BrandsConfig(AppConfig):
    """Configuration for the brands app.

    Purpose: Product brands (Apple, Samsung, Sony, etc.).
    """
    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.brands"
    verbose_name = "Brands"
