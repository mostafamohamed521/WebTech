"""
Service layer for the users app.

All business logic for updating a user's account/profile lives here —
views only orchestrate; they never touch model fields directly.
"""
from django.db import transaction

from .models import User, UserProfile


class UserService:
    @staticmethod
    def get_or_create_profile(user: User) -> UserProfile:
        profile, _ = UserProfile.objects.get_or_create(user=user)
        return profile

    @staticmethod
    @transaction.atomic
    def update_profile(user: User, data: dict) -> User:
        user_fields = {"first_name", "last_name", "phone", "avatar"}
        profile_fields = {"gender", "birth_date", "country", "city", "language"}

        for field in user_fields & data.keys():
            setattr(user, field, data[field])
        user.save(update_fields=list(user_fields & data.keys()) or None)

        profile = UserService.get_or_create_profile(user)
        changed = []
        for field in profile_fields & data.keys():
            setattr(profile, field, data[field])
            changed.append(field)
        if changed:
            profile.save(update_fields=changed)

        return user
