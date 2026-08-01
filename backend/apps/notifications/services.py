"""
Service layer for the notifications app.

Other apps call NotificationService.notify(...) directly (no signals/
event bus in this scaffold — kept explicit and easy to trace) whenever
something notification-worthy happens: order placed, order status
changed, review posted, etc.
"""
from .models import Notification, NotificationSettings


class NotificationService:
    @staticmethod
    def notify(user, title: str, body: str = "", type: str = Notification.Type.SYSTEM,
               priority: str = Notification.Priority.NORMAL, link: str = "") -> Notification:
        settings, _ = NotificationSettings.objects.get_or_create(user=user)
        if type == Notification.Type.ORDER and not settings.order_updates:
            return None
        if type == Notification.Type.PROMOTION and not settings.promotions:
            return None
        return Notification.objects.create(
            user=user, type=type, title=title, body=body, priority=priority, link=link,
        )

    @staticmethod
    def list_for_user(user, unread_only: bool = False):
        qs = Notification.objects.filter(user=user, is_deleted=False)
        if unread_only:
            qs = qs.filter(read=False)
        return qs

    @staticmethod
    def unread_count(user) -> int:
        return Notification.objects.filter(user=user, read=False, is_deleted=False).count()

    @staticmethod
    def mark_read(user, notification_id):
        Notification.objects.filter(id=notification_id, user=user).update(read=True)

    @staticmethod
    def mark_all_read(user):
        Notification.objects.filter(user=user, read=False).update(read=True)

    @staticmethod
    def get_or_create_settings(user) -> NotificationSettings:
        settings, _ = NotificationSettings.objects.get_or_create(user=user)
        return settings

    @staticmethod
    def update_settings(user, data: dict) -> NotificationSettings:
        settings = NotificationService.get_or_create_settings(user)
        for field, value in data.items():
            setattr(settings, field, value)
        settings.save()
        return settings
