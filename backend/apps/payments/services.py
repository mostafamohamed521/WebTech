"""
Service layer for the payments app.

COD is fully functional. Stripe/PayPal are wired as pluggable gateways
— swap `_charge_via_gateway` for a real SDK call when credentials are
available; the order/payment state machine around it stays the same.
"""
from .models import Payment


class PaymentService:
    @staticmethod
    def create_for_order(order, method: str = "cod") -> Payment:
        payment = Payment.objects.create(
            order=order,
            gateway=method,
            amount=order.grand_total,
            currency="EGP",
            status=Payment.Status.PENDING,
        )

        if method == Payment.Gateway.COD:
            # Cash collected on delivery — payment stays "pending" until
            # the courier confirms; order can still proceed as confirmed.
            payment.status = Payment.Status.PENDING
            payment.save(update_fields=["status"])
            order.payment_status = order.PaymentStatus.UNPAID
            order.status = order.Status.CONFIRMED
            order.save(update_fields=["payment_status", "status"])
            return payment

        # Online gateways (Stripe/PayPal): attempt an immediate charge.
        success, reference = PaymentService._charge_via_gateway(method, order)
        payment.status = Payment.Status.SUCCEEDED if success else Payment.Status.FAILED
        payment.reference = reference
        payment.save(update_fields=["status", "reference"])

        order.payment_status = order.PaymentStatus.PAID if success else order.PaymentStatus.FAILED
        order.status = order.Status.CONFIRMED if success else order.Status.PENDING
        order.save(update_fields=["payment_status", "status"])
        return payment

    @staticmethod
    def _charge_via_gateway(method: str, order) -> tuple[bool, str]:
        """
        Placeholder gateway integration point.
        TODO: replace with real Stripe (`stripe.PaymentIntent.create(...)`)
        or PayPal SDK calls once API keys are configured in .env.
        """
        return False, f"{method}_not_configured"
