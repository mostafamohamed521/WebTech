from rest_framework import serializers
from apps.addresses.serializers import AddressSerializer
from .models import Order, OrderItem, OrderStatusHistory


class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = ["id", "product", "variant", "product_name_snapshot", "quantity", "unit_price", "discount", "subtotal"]


class OrderStatusHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderStatusHistory
        fields = ["status", "note", "created_at"]


class OrderListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ["id", "order_number", "status", "payment_status", "grand_total", "created_at"]


class OrderDetailSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, read_only=True)
    status_history = OrderStatusHistorySerializer(many=True, read_only=True)
    address = AddressSerializer(read_only=True)

    class Meta:
        model = Order
        fields = [
            "id", "order_number", "status", "payment_status", "shipping_status",
            "address", "subtotal", "tax", "discount", "shipping_cost", "grand_total",
            "items", "status_history", "created_at",
        ]


class CheckoutSerializer(serializers.Serializer):
    address_id = serializers.UUIDField()
    coupon_code = serializers.CharField(required=False, allow_blank=True, default=None)
    payment_method = serializers.ChoiceField(choices=["cod", "stripe", "paypal"], default="cod")
