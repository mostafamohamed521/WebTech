from rest_framework import serializers
from .models import Payment


class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = ["id", "gateway", "status", "amount", "currency", "transaction_id", "created_at"]
