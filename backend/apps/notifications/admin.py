from django.contrib import admin
from .models import Notification, NotificationSettings


@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ("title", "user", "type", "read", "priority", "created_at")
    list_filter = ("type", "read", "priority")
    search_fields = ("title", "user__email")


@admin.register(NotificationSettings)
class NotificationSettingsAdmin(admin.ModelAdmin):
    list_display = ("user", "email_enabled", "push_enabled", "order_updates")
