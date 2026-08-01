"""
Views for the payments app.
"""
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView

from common.utils.responses import success_response, error_response
from .models import Payment
from .serializers import PaymentSerializer


class OrderPaymentsView(APIView):
    """GET /api/v1/payments/order/<order_number>/"""
    permission_classes = [IsAuthenticated]

    def get(self, request, order_number):
        payments = Payment.objects.filter(
            order__order_number=order_number, order__customer=request.user
        )
        if not payments.exists():
            return error_response(message="No payments found for this order", status=404)
        return success_response(PaymentSerializer(payments, many=True).data, message="Payments")
