"""
Serializers for the users app.
"""
from rest_framework import serializers

from .models import User, UserProfile


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ["gender", "birth_date", "country", "city", "language", "timezone"]


class UserSerializer(serializers.ModelSerializer):
    profile = UserProfileSerializer(read_only=True)

    class Meta:
        model = User
        fields = [
            "id", "email", "username", "first_name", "last_name",
            "phone", "avatar", "role", "is_email_verified", "profile", "created_at",
        ]
        read_only_fields = ["id", "email", "role", "is_email_verified", "created_at"]


class UpdateProfileSerializer(serializers.Serializer):
    first_name = serializers.CharField(required=False, allow_blank=True)
    last_name = serializers.CharField(required=False, allow_blank=True)
    phone = serializers.CharField(required=False, allow_blank=True)
    avatar = serializers.URLField(required=False, allow_blank=True)
    gender = serializers.ChoiceField(choices=UserProfile.Gender.choices, required=False)
    birth_date = serializers.DateField(required=False, allow_null=True)
    country = serializers.CharField(required=False, allow_blank=True)
    city = serializers.CharField(required=False, allow_blank=True)
    language = serializers.CharField(required=False)
