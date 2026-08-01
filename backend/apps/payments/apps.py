from django.apps import AppConfig


class PaymentsConfig(AppConfig):
    """Configuration for the payments app.

    Purpose: Payment transactions, gateways (Stripe/PayPal/COD).
    """
    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.payments"
    verbose_name = "Payments"
