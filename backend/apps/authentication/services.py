"""
Service layer for the authentication app.

All auth business rules live here: registration, login, logout
(single + all devices), password change/reset. Views stay thin.
"""
from django.contrib.auth import authenticate
from django.contrib.auth.tokens import default_token_generator
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from rest_framework.exceptions import AuthenticationFailed
from rest_framework_simplejwt.tokens import RefreshToken, OutstandingToken, BlacklistedToken

from apps.users.models import User
from common.emails.tasks import send_welcome_email


class AuthService:
    @staticmethod
    def register(data: dict) -> tuple[User, dict]:
        user = User.objects.create_user(
            email=data["email"],
            username=data["username"],
            password=data["password"],
            first_name=data.get("first_name", ""),
            last_name=data.get("last_name", ""),
            phone=data.get("phone", ""),
        )
        tokens = AuthService.issue_tokens(user)
        try:
            send_welcome_email.delay(user.email, user.first_name or user.username)
        except Exception:
            # Celery/broker not running in this environment — non-fatal.
            pass
        return user, tokens

    @staticmethod
    def login(email: str, password: str, session_key: str | None = None) -> tuple[User, dict]:
        user = authenticate(username=email, password=password)
        if user is None:
            raise AuthenticationFailed("Invalid email or password.")
        if not user.is_active:
            raise AuthenticationFailed("This account has been disabled.")
        if session_key:
            from apps.cart.services import CartService
            CartService.merge_guest_cart_into_user(user, session_key)
        tokens = AuthService.issue_tokens(user)
        return user, tokens

    @staticmethod
    def issue_tokens(user: User) -> dict:
        refresh = RefreshToken.for_user(user)
        return {"access": str(refresh.access_token), "refresh": str(refresh)}

    @staticmethod
    def logout(refresh_token: str):
        token = RefreshToken(refresh_token)
        token.blacklist()

    @staticmethod
    def logout_all_devices(user: User):
        tokens = OutstandingToken.objects.filter(user=user)
        for token in tokens:
            BlacklistedToken.objects.get_or_create(token=token)

    @staticmethod
    def change_password(user: User, old_password: str, new_password: str):
        if not user.check_password(old_password):
            raise AuthenticationFailed("Current password is incorrect.")
        user.set_password(new_password)
        user.save(update_fields=["password"])

    @staticmethod
    def request_password_reset(email: str) -> tuple[User, str, str] | None:
        try:
            user = User.objects.get(email__iexact=email)
        except User.DoesNotExist:
            return None
        uid = urlsafe_base64_encode(force_bytes(user.pk))
        token = default_token_generator.make_token(user)
        # TODO: wire to common.emails.tasks.send_password_reset_email(user.email, uid, token)
        return user, uid, token

    @staticmethod
    def reset_password(uid: str, token: str, new_password: str):
        try:
            user_id = force_str(urlsafe_base64_decode(uid))
            user = User.objects.get(pk=user_id)
        except (User.DoesNotExist, ValueError, TypeError, OverflowError):
            raise AuthenticationFailed("Invalid reset link.")
        if not default_token_generator.check_token(user, token):
            raise AuthenticationFailed("Invalid or expired reset link.")
        user.set_password(new_password)
        user.save(update_fields=["password"])
