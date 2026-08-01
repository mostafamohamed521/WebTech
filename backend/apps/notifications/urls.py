from django.urls import path
from .views import (
    NotificationListView, MarkNotificationReadView, MarkAllNotificationsReadView, NotificationSettingsView,
)

app_name = "notifications"

urlpatterns = [
    path("", NotificationListView.as_view(), name="list"),
    path("<uuid:pk>/read/", MarkNotificationReadView.as_view(), name="mark-read"),
    path("mark-all-read/", MarkAllNotificationsReadView.as_view(), name="mark-all-read"),
    path("settings/", NotificationSettingsView.as_view(), name="settings"),
]
