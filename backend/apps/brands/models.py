"""
Models for the brands app.
"""
from django.db import models
from common.models import BaseModel


class Brand(BaseModel):
    name = models.CharField(max_length=150, unique=True, db_index=True)
    slug = models.SlugField(max_length=170, unique=True, db_index=True)
    logo = models.URLField(blank=True)
    description = models.TextField(blank=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        db_table = "brands"
        indexes = [models.Index(fields=["slug"])]
        ordering = ["name"]

    def __str__(self):
        return self.name
