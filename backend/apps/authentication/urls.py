"""
URL routes for the authentication app. Mounted under /api/v1/authentication/.
"""
from django.urls import path
from .views import (
    RegisterView, LoginView, LogoutView, LogoutAllDevicesView, TokenRefreshView,
    ChangePasswordView, RequestPasswordResetView, ResetPasswordView,
)

app_name = "authentication"

urlpatterns = [
    path("register/", RegisterView.as_view(), name="register"),
    path("login/", LoginView.as_view(), name="login"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("logout-all/", LogoutAllDevicesView.as_view(), name="logout-all"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token-refresh"),
    path("change-password/", ChangePasswordView.as_view(), name="change-password"),
    path("password-reset/", RequestPasswordResetView.as_view(), name="password-reset"),
    path("password-reset/confirm/", ResetPasswordView.as_view(), name="password-reset-confirm"),
]
