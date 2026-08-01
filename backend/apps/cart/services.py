"""
Service layer for the cart app: guest cart, user cart, merge on login,
add/update/remove items, subtotal + coupon-aware totals.
"""
from django.db import transaction
from rest_framework.exceptions import ValidationError

from apps.products.models import Product, ProductVariant
from .models import ShoppingCart, CartItem


class CartService:
    @staticmethod
    def get_or_create_cart(user=None, session_key=None) -> ShoppingCart:
        if user and user.is_authenticated:
            cart, _ = ShoppingCart.objects.get_or_create(user=user)
            return cart
        cart, _ = ShoppingCart.objects.get_or_create(session_key=session_key)
        return cart

    @staticmethod
    @transaction.atomic
    def merge_guest_cart_into_user(user, session_key: str):
        """Called right after login: fold a guest session cart into the user's cart."""
        if not session_key:
            return
        try:
            guest_cart = ShoppingCart.objects.get(session_key=session_key, user__isnull=True)
        except ShoppingCart.DoesNotExist:
            return

        user_cart, _ = ShoppingCart.objects.get_or_create(user=user)
        for item in guest_cart.items.all():
            existing = CartItem.objects.filter(cart=user_cart, product=item.product, variant=item.variant).first()
            if existing:
                existing.quantity += item.quantity
                existing.save(update_fields=["quantity"])
            else:
                item.cart = user_cart
                item.save(update_fields=["cart"])
        guest_cart.delete()

    @staticmethod
    @transaction.atomic
    def add_item(cart: ShoppingCart, product_id, variant_id, quantity: int) -> CartItem:
        try:
            product = Product.objects.get(id=product_id, published=True, is_deleted=False)
        except Product.DoesNotExist:
            raise ValidationError({"product_id": ["Product not found."]})

        variant = None
        unit_price = product.effective_price
        if variant_id:
            try:
                variant = ProductVariant.objects.get(id=variant_id, product=product, is_deleted=False)
                unit_price += variant.price_difference
            except ProductVariant.DoesNotExist:
                raise ValidationError({"variant_id": ["Variant not found for this product."]})

        available_stock = variant.stock if variant else product.stock
        item, created = CartItem.objects.get_or_create(
            cart=cart, product=product, variant=variant,
            defaults={"quantity": quantity, "price": unit_price},
        )
        if not created:
            item.quantity += quantity

        if item.quantity > available_stock:
            raise ValidationError({"quantity": [f"Only {available_stock} in stock."]})

        item.price = unit_price
        item.save()
        return item

    @staticmethod
    def update_item(cart: ShoppingCart, item_id, quantity: int) -> CartItem:
        try:
            item = CartItem.objects.get(id=item_id, cart=cart)
        except CartItem.DoesNotExist:
            raise ValidationError({"item": ["Cart item not found."]})

        available_stock = item.variant.stock if item.variant else item.product.stock
        if quantity > available_stock:
            raise ValidationError({"quantity": [f"Only {available_stock} in stock."]})

        item.quantity = quantity
        item.save(update_fields=["quantity"])
        return item

    @staticmethod
    def remove_item(cart: ShoppingCart, item_id):
        CartItem.objects.filter(id=item_id, cart=cart).delete()

    @staticmethod
    def clear(cart: ShoppingCart):
        cart.items.all().delete()
        cart.coupon = None
        cart.save(update_fields=["coupon"])

    @staticmethod
    def subtotal(cart: ShoppingCart):
        return sum((item.subtotal for item in cart.items.all()), start=0)

    @staticmethod
    def apply_coupon(cart: ShoppingCart, coupon):
        cart.coupon = coupon
        cart.save(update_fields=["coupon"])
