from django.apps import AppConfig


class AuthenticationConfig(AppConfig):
    """Configuration for the authentication app.

    Purpose: Handles register, login, JWT tokens, email verification, password reset, logout (all devices), social login hooks.
    """
    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.authentication"
    verbose_name = "Authentication"
