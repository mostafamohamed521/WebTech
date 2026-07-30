"""
Models for the addresses app: user shipping/billing addresses.
"""
from django.db import models
from common.models import BaseModel
from apps.users.models import User


class Address(BaseModel):
    class AddressType(models.TextChoices):
        SHIPPING = "shipping", "Shipping"
        BILLING = "billing", "Billing"
        BOTH = "both", "Both"

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="addresses")
    label = models.CharField(max_length=50, blank=True)  # e.g. "Home", "Office"
    type = models.CharField(max_length=10, choices=AddressType.choices, default=AddressType.BOTH)
    full_name = models.CharField(max_length=150)
    phone = models.CharField(max_length=32)
    country = models.CharField(max_length=100, default="Egypt")
    city = models.CharField(max_length=100)
    street = models.CharField(max_length=255)
    building = models.CharField(max_length=50, blank=True)
    apartment = models.CharField(max_length=50, blank=True)
    postal_code = models.CharField(max_length=20, blank=True)
    latitude = models.DecimalField(max_digits=10, decimal_places=7, null=True, blank=True)
    longitude = models.DecimalField(max_digits=10, decimal_places=7, null=True, blank=True)
    is_default = models.BooleanField(default=False)

    class Meta:
        db_table = "user_addresses"
        indexes = [models.Index(fields=["user"])]
        ordering = ["-is_default", "-created_at"]

    def __str__(self):
        return f"{self.label or self.city} — {self.user.email}"
