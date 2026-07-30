"""
Models for the categories app: category tree (with sub-categories via self-FK).
"""
from django.db import models
from common.models import BaseModel


class Category(BaseModel):
    name = models.CharField(max_length=150, db_index=True)
    slug = models.SlugField(max_length=170, unique=True, db_index=True)
    parent = models.ForeignKey(
        "self", null=True, blank=True, on_delete=models.CASCADE, related_name="children"
    )
    image = models.URLField(blank=True)
    is_active = models.BooleanField(default=True)
    sort_order = models.PositiveIntegerField(default=0)

    class Meta:
        db_table = "categories"
        verbose_name_plural = "categories"
        indexes = [models.Index(fields=["slug"]), models.Index(fields=["parent"])]
        ordering = ["sort_order", "name"]

    def __str__(self):
        return self.name
