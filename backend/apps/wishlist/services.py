"""
Service layer for the wishlist app.
"""
from rest_framework.exceptions import ValidationError
from apps.products.models import Product
from .models import Wishlist, WishlistItem


class WishlistService:
    @staticmethod
    def get_or_create(user) -> Wishlist:
        wishlist, _ = Wishlist.objects.get_or_create(user=user)
        return wishlist

    @staticmethod
    def add(user, product_id) -> WishlistItem:
        wishlist = WishlistService.get_or_create(user)
        try:
            product = Product.objects.get(id=product_id, is_deleted=False)
        except Product.DoesNotExist:
            raise ValidationError({"product_id": ["Product not found."]})
        item, _ = WishlistItem.objects.get_or_create(wishlist=wishlist, product=product)
        return item

    @staticmethod
    def remove(user, product_id):
        wishlist = WishlistService.get_or_create(user)
        WishlistItem.objects.filter(wishlist=wishlist, product_id=product_id).delete()

    @staticmethod
    def list_items(user):
        wishlist = WishlistService.get_or_create(user)
        return wishlist.items.select_related("product").all()
