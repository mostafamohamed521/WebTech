"""
Models for the users app.

Custom User model (email-based login) + role system + profile, per
WEBTECH auth spec: Super Admin, Admin, Manager, Support, Customer.
"""
import uuid
from django.contrib.auth.models import AbstractUser
from django.db import models

from common.models import BaseModel


class Role(models.TextChoices):
    SUPER_ADMIN = "super_admin", "Super Admin"
    ADMIN = "admin", "Admin"
    MANAGER = "manager", "Manager"
    SUPPORT = "support", "Support"
    CUSTOMER = "customer", "Customer"


class User(AbstractUser):
    """Custom user: login by email, carries a WEBTECH role."""
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email = models.EmailField(unique=True, db_index=True)
    phone = models.CharField(max_length=32, blank=True, db_index=True)
    avatar = models.URLField(blank=True)
    role = models.CharField(max_length=20, choices=Role.choices, default=Role.CUSTOMER, db_index=True)
    is_email_verified = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]

    class Meta:
        db_table = "users"
        indexes = [
            models.Index(fields=["email"]),
            models.Index(fields=["phone"]),
            models.Index(fields=["role"]),
        ]

    def __str__(self):
        return self.email

    @property
    def is_staff_role(self):
        return self.role in {Role.SUPER_ADMIN, Role.ADMIN, Role.MANAGER, Role.SUPPORT}


class UserProfile(BaseModel):
    class Gender(models.TextChoices):
        MALE = "male", "Male"
        FEMALE = "female", "Female"
        OTHER = "other", "Other"

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile")
    gender = models.CharField(max_length=10, choices=Gender.choices, blank=True)
    birth_date = models.DateField(null=True, blank=True)
    country = models.CharField(max_length=100, blank=True)
    city = models.CharField(max_length=100, blank=True)
    language = models.CharField(max_length=10, default="ar")
    timezone = models.CharField(max_length=50, default="Africa/Cairo")

    class Meta:
        db_table = "user_profiles"

    def __str__(self):
        return f"Profile<{self.user.email}>"
