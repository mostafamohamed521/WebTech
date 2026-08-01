"""
Models for the cart app: guest + user shopping cart.
"""
from django.db import models
from common.models import BaseModel
from apps.users.models import User
from apps.products.models import Product, ProductVariant
from apps.coupons.models import Coupon


class ShoppingCart(BaseModel):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="cart", null=True, blank=True)
    session_key = models.CharField(max_length=64, null=True, blank=True, db_index=True)
    coupon = models.ForeignKey(Coupon, on_delete=models.SET_NULL, null=True, blank=True)
    currency = models.CharField(max_length=3, default="EGP")

    class Meta:
        db_table = "shopping_carts"
        indexes = [models.Index(fields=["session_key"])]

    def __str__(self):
        return f"Cart<{self.user or self.session_key}>"


class CartItem(BaseModel):
    cart = models.ForeignKey(ShoppingCart, on_delete=models.CASCADE, related_name="items")
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    variant = models.ForeignKey(ProductVariant, on_delete=models.SET_NULL, null=True, blank=True)
    quantity = models.PositiveIntegerField(default=1)
    price = models.DecimalField(max_digits=12, decimal_places=2)  # unit price snapshot at add-time

    class Meta:
        db_table = "cart_items"
        unique_together = ("cart", "product", "variant")

    @property
    def subtotal(self):
        return self.price * self.quantity
