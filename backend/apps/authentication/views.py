"""
Views for the authentication app.
"""
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.views import APIView
from rest_framework_simplejwt.views import TokenRefreshView as SimpleJWTRefreshView

from apps.users.serializers import UserSerializer
from common.utils.responses import success_response, error_response
from .serializers import (
    RegisterSerializer, LoginSerializer, ChangePasswordSerializer,
    RequestPasswordResetSerializer, ResetPasswordSerializer,
)
from .services import AuthService


class RegisterView(APIView):
    permission_classes = [AllowAny]
    throttle_scope = "auth"

    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if not serializer.is_valid():
            return error_response(serializer.errors, message="Registration failed")
        session_key = request.headers.get("X-Session-Key")
        user, tokens = AuthService.register(serializer.validated_data, session_key=session_key)
        return success_response(
            {"user": UserSerializer(user).data, "tokens": tokens},
            message="Account created successfully", status=201,
        )


class LoginView(APIView):
    permission_classes = [AllowAny]
    throttle_scope = "auth"

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if not serializer.is_valid():
            return error_response(serializer.errors, message="Login failed")
        session_key = request.headers.get("X-Session-Key")
        user, tokens = AuthService.login(**serializer.validated_data, session_key=session_key)
        return success_response(
            {"user": UserSerializer(user).data, "tokens": tokens},
            message="Logged in successfully",
        )


class LogoutView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        refresh = request.data.get("refresh")
        if not refresh:
            return error_response({"refresh": ["This field is required."]}, message="Logout failed")
        AuthService.logout(refresh)
        return success_response(message="Logged out successfully")


class LogoutAllDevicesView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        AuthService.logout_all_devices(request.user)
        return success_response(message="Logged out from all devices")


class TokenRefreshView(SimpleJWTRefreshView):
    """Thin wrapper so refresh also follows the WEBTECH response envelope."""

    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)
        if response.status_code == 200:
            return success_response(response.data, message="Token refreshed")
        return error_response(response.data, message="Token refresh failed", status=response.status_code)


class ChangePasswordView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = ChangePasswordSerializer(data=request.data)
        if not serializer.is_valid():
            return error_response(serializer.errors, message="Invalid input")
        AuthService.change_password(request.user, **serializer.validated_data)
        return success_response(message="Password changed successfully")


class RequestPasswordResetView(APIView):
    permission_classes = [AllowAny]
    throttle_scope = "auth"

    def post(self, request):
        serializer = RequestPasswordResetSerializer(data=request.data)
        if not serializer.is_valid():
            return error_response(serializer.errors, message="Invalid input")
        AuthService.request_password_reset(serializer.validated_data["email"])
        # Always return success to avoid leaking which emails are registered.
        return success_response(message="If that email exists, a reset link has been sent")


class ResetPasswordView(APIView):
    permission_classes = [AllowAny]
    throttle_scope = "auth"

    def post(self, request):
        serializer = ResetPasswordSerializer(data=request.data)
        if not serializer.is_valid():
            return error_response(serializer.errors, message="Invalid input")
        AuthService.reset_password(**serializer.validated_data)
        return success_response(message="Password reset successfully")
