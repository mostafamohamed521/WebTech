"""
Views for the analytics app — admin only.
"""
from rest_framework.views import APIView

from common.permissions.roles import IsAdmin
from common.utils.responses import success_response
from .serializers import AnalyticsOverviewSerializer
from .services import AnalyticsService


class AnalyticsOverviewView(APIView):
    """GET /api/v1/analytics/overview/?days=30"""
    permission_classes = [IsAdmin]

    def get(self, request):
        days = min(int(request.query_params.get("days", 30)), 365)
        data = AnalyticsService.overview(days=days)
        return success_response(AnalyticsOverviewSerializer(data).data, message="Analytics overview")
