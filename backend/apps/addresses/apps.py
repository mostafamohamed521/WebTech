from django.apps import AppConfig


class AddressesConfig(AppConfig):
    """Configuration for the addresses app.

    Purpose: Shipping and billing addresses for users.
    """
    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.addresses"
    verbose_name = "Addresses"
