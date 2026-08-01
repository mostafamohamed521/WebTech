from django.apps import AppConfig


class SupportConfig(AppConfig):
    """Configuration for the support app.

    Purpose: Support tickets and ticket replies.
    """
    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.support"
    verbose_name = "Support"
