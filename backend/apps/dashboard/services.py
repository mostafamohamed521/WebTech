"""
Service layer for the dashboard app: stats aggregation and admin
product/order management operations.
"""
from datetime import timedelta
from django.db.models import Sum, Count
from django.utils import timezone

from apps.orders.models import Order, OrderStatusHistory
from apps.products.models import Product
from apps.users.models import User


class DashboardService:
    LOW_STOCK_THRESHOLD = 5

    @staticmethod
    def get_stats() -> dict:
        paid_orders = Order.objects.exclude(status=Order.Status.CANCELLED)

        total_revenue = paid_orders.aggregate(total=Sum("grand_total"))["total"] or 0
        total_orders = Order.objects.count()
        total_products = Product.objects.filter(is_deleted=False).count()
        total_customers = User.objects.filter(role="customer").count()

        orders_by_status = {
            row["status"]: row["count"]
            for row in Order.objects.values("status").annotate(count=Count("id"))
        }

        today = timezone.now().date()
        revenue_last_7_days = []
        for i in range(6, -1, -1):
            day = today - timedelta(days=i)
            day_total = paid_orders.filter(created_at__date=day).aggregate(total=Sum("grand_total"))["total"] or 0
            revenue_last_7_days.append({"date": day.isoformat(), "revenue": float(day_total)})

        low_stock = list(
            Product.objects.filter(stock__lte=DashboardService.LOW_STOCK_THRESHOLD, is_deleted=False, published=True)
            .order_by("stock")
            .values("id", "name", "sku", "stock")[:10]
        )
        for p in low_stock:
            p["id"] = str(p["id"])

        return {
            "total_revenue": total_revenue,
            "total_orders": total_orders,
            "total_products": total_products,
            "total_customers": total_customers,
            "orders_by_status": orders_by_status,
            "revenue_last_7_days": revenue_last_7_days,
            "low_stock_products": low_stock,
        }

    @staticmethod
    def update_order_status(order: Order, status: str, note: str = ""):
        order.status = status
        order.save(update_fields=["status"])
        OrderStatusHistory.objects.create(order=order, status=status, note=note or f"Status updated to {status} by admin")

        from apps.notifications.services import NotificationService
        from apps.notifications.models import Notification
        NotificationService.notify(
            order.customer, title=f"Order {order.order_number} — {status}",
            body=note or f"Your order status changed to {status}.",
            type=Notification.Type.ORDER, link=f"/account/orders/{order.order_number}",
        )
        return order
