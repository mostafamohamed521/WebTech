"""
Models for the search app: search history + popularity tracking.
"""
from django.db import models
from common.models import BaseModel
from apps.users.models import User


class SearchHistory(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="search_history", null=True, blank=True)
    session_key = models.CharField(max_length=64, blank=True, db_index=True)
    keyword = models.CharField(max_length=255, db_index=True)
    results_count = models.PositiveIntegerField(default=0)

    class Meta:
        db_table = "search_history"
        indexes = [models.Index(fields=["keyword"])]
        ordering = ["-created_at"]

    def __str__(self):
        return self.keyword
