from django.apps import AppConfig


class AnalyticsConfig(AppConfig):
    """Configuration for the analytics app.

    Purpose: Sales, revenue, traffic and conversion analytics.
    """
    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.analytics"
    verbose_name = "Analytics"
