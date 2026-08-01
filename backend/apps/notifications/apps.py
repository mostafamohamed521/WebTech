from django.apps import AppConfig


class NotificationsConfig(AppConfig):
    """Configuration for the notifications app.

    Purpose: In-app and email notifications, notification settings.
    """
    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.notifications"
    verbose_name = "Notifications"
