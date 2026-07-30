"""
Service layer for the addresses app.
"""
from django.db import transaction
from .models import Address


class AddressService:
    @staticmethod
    def list_for_user(user):
        return Address.objects.filter(user=user, is_deleted=False)

    @staticmethod
    @transaction.atomic
    def create(user, data: dict) -> Address:
        if data.get("is_default"):
            Address.objects.filter(user=user, is_default=True).update(is_default=False)
        return Address.objects.create(user=user, **data)

    @staticmethod
    @transaction.atomic
    def update(address: Address, data: dict) -> Address:
        if data.get("is_default"):
            Address.objects.filter(user=address.user, is_default=True).exclude(id=address.id).update(is_default=False)
        for field, value in data.items():
            setattr(address, field, value)
        address.save()
        return address

    @staticmethod
    def delete(address: Address):
        address.soft_delete()
