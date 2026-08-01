from django.apps import AppConfig


class OrdersConfig(AppConfig):
    """Configuration for the orders app.

    Purpose: Order creation, order items, status history, invoices.
    """
    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.orders"
    verbose_name = "Orders"
