"""
Views for the notifications app.
"""
from django.core.paginator import Paginator
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView

from common.utils.responses import success_response, error_response
from .serializers import NotificationSerializer, NotificationSettingsSerializer
from .services import NotificationService


class NotificationListView(APIView):
    """GET /api/v1/notifications/?unread=true"""
    permission_classes = [IsAuthenticated]

    def get(self, request):
        unread_only = request.query_params.get("unread") == "true"
        qs = NotificationService.list_for_user(request.user, unread_only=unread_only)

        page_size = min(int(request.query_params.get("page_size", 20)), 100)
        paginator = Paginator(qs, page_size)
        page = paginator.get_page(request.query_params.get("page", 1))

        return success_response(
            {
                "results": NotificationSerializer(page.object_list, many=True).data,
                "count": paginator.count,
                "unread_count": NotificationService.unread_count(request.user),
            },
            message="Notifications",
        )


class MarkNotificationReadView(APIView):
    """PATCH /api/v1/notifications/<id>/read/"""
    permission_classes = [IsAuthenticated]

    def patch(self, request, pk):
        NotificationService.mark_read(request.user, pk)
        return success_response(message="Marked as read")


class MarkAllNotificationsReadView(APIView):
    """POST /api/v1/notifications/mark-all-read/"""
    permission_classes = [IsAuthenticated]

    def post(self, request):
        NotificationService.mark_all_read(request.user)
        return success_response(message="All notifications marked as read")


class NotificationSettingsView(APIView):
    """GET/PATCH /api/v1/notifications/settings/"""
    permission_classes = [IsAuthenticated]

    def get(self, request):
        settings = NotificationService.get_or_create_settings(request.user)
        return success_response(NotificationSettingsSerializer(settings).data, message="Notification settings")

    def patch(self, request):
        serializer = NotificationSettingsSerializer(data=request.data, partial=True)
        if not serializer.is_valid():
            return error_response(serializer.errors, message="Invalid settings")
        settings = NotificationService.update_settings(request.user, serializer.validated_data)
        return success_response(NotificationSettingsSerializer(settings).data, message="Settings updated")
