"""
Views for the orders app.
"""
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView

from common.utils.responses import success_response, error_response
from .serializers import CheckoutSerializer, OrderListSerializer, OrderDetailSerializer
from .services import OrderService


class CheckoutView(APIView):
    """POST /api/v1/orders/checkout/ — turns the current cart into an order."""
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = CheckoutSerializer(data=request.data)
        if not serializer.is_valid():
            return error_response(serializer.errors, message="Invalid checkout data")
        order = OrderService.checkout(request.user, **serializer.validated_data)
        return success_response(OrderDetailSerializer(order).data, message="Order placed successfully", status=201)


class OrderListView(APIView):
    """GET /api/v1/orders/"""
    permission_classes = [IsAuthenticated]

    def get(self, request):
        orders = OrderService.list_for_user(request.user)
        return success_response(OrderListSerializer(orders, many=True).data, message="Orders")


class OrderDetailView(APIView):
    """GET /api/v1/orders/<order_number>/"""
    permission_classes = [IsAuthenticated]

    def get(self, request, order_number):
        try:
            order = OrderService.get_for_user(request.user, order_number)
        except Exception:
            return error_response(message="Order not found", status=404)
        return success_response(OrderDetailSerializer(order).data, message="Order detail")
