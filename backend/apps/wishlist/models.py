"""
Models for the wishlist app.
"""
from django.db import models
from common.models import BaseModel
from apps.users.models import User
from apps.products.models import Product


class Wishlist(BaseModel):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="wishlist")

    class Meta:
        db_table = "wishlists"


class WishlistItem(BaseModel):
    wishlist = models.ForeignKey(Wishlist, on_delete=models.CASCADE, related_name="items")
    product = models.ForeignKey(Product, on_delete=models.CASCADE)

    class Meta:
        db_table = "wishlist_items"
        unique_together = ("wishlist", "product")
