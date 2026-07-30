"""
Views for the users app.
"""
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView

from common.utils.responses import success_response, error_response
from .serializers import UserSerializer, UpdateProfileSerializer
from .services import UserService


class MeView(APIView):
    """GET /api/v1/users/me/  — current user's account + profile.
    PATCH /api/v1/users/me/ — update account + profile fields.
    """
    permission_classes = [IsAuthenticated]

    def get(self, request):
        return success_response(UserSerializer(request.user).data, message="Current user")

    def patch(self, request):
        serializer = UpdateProfileSerializer(data=request.data, partial=True)
        if not serializer.is_valid():
            return error_response(serializer.errors, message="Invalid profile data")
        user = UserService.update_profile(request.user, serializer.validated_data)
        return success_response(UserSerializer(user).data, message="Profile updated")
