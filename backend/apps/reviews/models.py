"""
Models for the reviews app.
"""
from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from common.models import BaseModel
from apps.users.models import User
from apps.products.models import Product


class Review(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="reviews")
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="reviews")
    rating = models.PositiveSmallIntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    comment = models.TextField(blank=True)
    verified_purchase = models.BooleanField(default=False)
    helpful_count = models.PositiveIntegerField(default=0)

    class Meta:
        db_table = "reviews"
        unique_together = ("user", "product")
        indexes = [models.Index(fields=["product"])]
        ordering = ["-helpful_count", "-created_at"]

    def __str__(self):
        return f"{self.rating}★ {self.product.name} by {self.user.email}"


class ReviewImage(BaseModel):
    review = models.ForeignKey(Review, on_delete=models.CASCADE, related_name="images")
    url = models.URLField()

    class Meta:
        db_table = "review_images"


class ReviewLike(BaseModel):
    review = models.ForeignKey(Review, on_delete=models.CASCADE, related_name="likes")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="review_likes")

    class Meta:
        db_table = "review_likes"
        unique_together = ("review", "user")
