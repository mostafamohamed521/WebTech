"""
Django admin registration for the users app.
"""
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as DjangoUserAdmin

from .models import User, UserProfile


@admin.register(User)
class UserAdmin(DjangoUserAdmin):
    ordering = ("-created_at",)
    list_display = ("email", "username", "role", "is_active", "is_email_verified", "created_at")
    list_filter = ("role", "is_active", "is_email_verified")
    search_fields = ("email", "username", "phone")
    fieldsets = DjangoUserAdmin.fieldsets + (
        ("WEBTECH", {"fields": ("role", "phone", "avatar", "is_email_verified")}),
    )


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ("user", "country", "city", "language")
    search_fields = ("user__email",)
