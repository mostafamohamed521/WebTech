from django.apps import AppConfig


class InventoryConfig(AppConfig):
    """Configuration for the inventory app.

    Purpose: Warehouses, stock levels, stock movement history.
    """
    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.inventory"
    verbose_name = "Inventory"
