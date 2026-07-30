"""
Models for the wishlist app.

Purpose: User wishlists and wishlist items.

NOTE: This is a clean-architecture scaffold. Models below define the
table shape only. All business rules live in services.py, never here.
"""
import uuid
from django.db import models


class BaseModel(models.Model):
    """Abstract base model shared across the project.

    Provides UUID primary key + timestamps + soft delete, per the
    WEBTECH database architecture spec.
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_deleted = models.BooleanField(default=False)

    class Meta:
        abstract = True


# TODO: Define wishlist models here (see /database/SCHEMA.md for full field list).
