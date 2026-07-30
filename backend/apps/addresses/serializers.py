from rest_framework import serializers
from .models import Address


class AddressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Address
        fields = [
            "id", "label", "type", "full_name", "phone", "country", "city",
            "street", "building", "apartment", "postal_code",
            "latitude", "longitude", "is_default",
        ]
