"""
Service layer for the orders app: checkout (cart -> order), inventory
reduction, order status transitions, invoice-ready order fetch.
"""
from decimal import Decimal
from django.db import transaction
from rest_framework.exceptions import ValidationError

from apps.addresses.models import Address
from apps.cart.services import CartService
from apps.coupons.services import CouponService
from .models import Order, OrderItem, OrderStatusHistory


class OrderService:
    SHIPPING_FLAT_RATE = Decimal("50.00")
    TAX_RATE = Decimal("0.14")  # 14% VAT (Egypt)

    @staticmethod
    @transaction.atomic
    def checkout(user, address_id, coupon_code: str | None, payment_method: str) -> Order:
        cart = CartService.get_or_create_cart(user=user)
        items = list(cart.items.select_related("product", "variant"))
        if not items:
            raise ValidationError({"cart": ["Your cart is empty."]})

        try:
            address = Address.objects.get(id=address_id, user=user, is_deleted=False)
        except Address.DoesNotExist:
            raise ValidationError({"address_id": ["Address not found."]})

        # Validate stock before committing anything.
        for item in items:
            available = item.variant.stock if item.variant else item.product.stock
            if item.quantity > available:
                raise ValidationError({"cart": [f"'{item.product.name}' only has {available} in stock."]})

        subtotal = CartService.subtotal(cart)

        discount = Decimal("0")
        coupon = None
        if coupon_code:
            coupon = CouponService.validate_and_get(coupon_code, user, subtotal)
            discount = coupon.calculate_discount(subtotal)

        tax = (subtotal - discount) * OrderService.TAX_RATE
        shipping_cost = OrderService.SHIPPING_FLAT_RATE
        grand_total = subtotal - discount + tax + shipping_cost

        order = Order.objects.create(
            customer=user,
            address=address,
            coupon=coupon,
            subtotal=subtotal,
            tax=tax,
            discount=discount,
            shipping_cost=shipping_cost,
            grand_total=grand_total,
        )

        for item in items:
            OrderItem.objects.create(
                order=order,
                product=item.product,
                variant=item.variant,
                product_name_snapshot=item.product.name,
                quantity=item.quantity,
                unit_price=item.price,
                subtotal=item.subtotal,
            )
            # Reduce inventory
            if item.variant:
                item.variant.stock -= item.quantity
                item.variant.save(update_fields=["stock"])
            else:
                item.product.stock -= item.quantity
                item.product.save(update_fields=["stock"])

        OrderStatusHistory.objects.create(order=order, status=Order.Status.PENDING, note="Order placed")

        if coupon:
            CouponService.record_usage(coupon, user, order)

        from apps.payments.services import PaymentService
        PaymentService.create_for_order(order, method=payment_method)

        CartService.clear(cart)
        return order

    @staticmethod
    def list_for_user(user):
        return Order.objects.filter(customer=user, is_deleted=False).order_by("-created_at")

    @staticmethod
    def get_for_user(user, order_number: str) -> Order:
        return Order.objects.select_related("address").prefetch_related(
            "items", "status_history"
        ).get(customer=user, order_number=order_number, is_deleted=False)

    @staticmethod
    @transaction.atomic
    def update_status(order: Order, status: str, note: str = ""):
        order.status = status
        order.save(update_fields=["status"])
        OrderStatusHistory.objects.create(order=order, status=status, note=note)
