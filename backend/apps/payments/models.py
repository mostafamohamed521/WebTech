"""
Models for the payments app.
"""
from django.db import models
from common.models import BaseModel
from apps.users.models import User


class Payment(BaseModel):
    class Gateway(models.TextChoices):
        COD = "cod", "Cash on Delivery"
        STRIPE = "stripe", "Stripe"
        PAYPAL = "paypal", "PayPal"

    class Status(models.TextChoices):
        PENDING = "pending", "Pending"
        SUCCEEDED = "succeeded", "Succeeded"
        FAILED = "failed", "Failed"
        REFUNDED = "refunded", "Refunded"

    order = models.ForeignKey("orders.Order", on_delete=models.CASCADE, related_name="payments")
    transaction_id = models.CharField(max_length=100, blank=True, db_index=True)
    gateway = models.CharField(max_length=20, choices=Gateway.choices)
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.PENDING)
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    currency = models.CharField(max_length=3, default="EGP")
    reference = models.CharField(max_length=255, blank=True)

    class Meta:
        db_table = "payments"
        indexes = [models.Index(fields=["transaction_id"])]

    def __str__(self):
        return f"Payment<{self.order.order_number}:{self.gateway}>"


class PaymentMethod(BaseModel):
    """Saved payment method for a user (tokenized — never store raw card data)."""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="payment_methods")
    type = models.CharField(max_length=20)
    provider_token = models.CharField(max_length=255)
    is_default = models.BooleanField(default=False)

    class Meta:
        db_table = "payment_methods"
