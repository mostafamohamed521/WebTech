"""
Service layer for the analytics app: deeper reporting than the
dashboard's headline stats — top products, sales by category, revenue
trend over a configurable window, new vs returning customers.
"""
from datetime import timedelta
from django.db.models import Sum, Count, F
from django.utils import timezone

from apps.orders.models import OrderItem, Order
from apps.users.models import User


class AnalyticsService:
    @staticmethod
    def top_selling_products(days: int = 30, limit: int = 10):
        since = timezone.now() - timedelta(days=days)
        rows = (
            OrderItem.objects.filter(order__created_at__gte=since, order__status__in=[
                "confirmed", "processing", "shipped", "delivered",
            ])
            .values("product__id", "product__name", "product__sku")
            .annotate(units_sold=Sum("quantity"), revenue=Sum(F("unit_price") * F("quantity")))
            .order_by("-units_sold")[:limit]
        )
        return [
            {
                "product_id": str(r["product__id"]),
                "name": r["product__name"],
                "sku": r["product__sku"],
                "units_sold": r["units_sold"],
                "revenue": float(r["revenue"] or 0),
            }
            for r in rows
        ]

    @staticmethod
    def sales_by_category(days: int = 30):
        since = timezone.now() - timedelta(days=days)
        rows = (
            OrderItem.objects.filter(order__created_at__gte=since, order__status__in=[
                "confirmed", "processing", "shipped", "delivered",
            ])
            .values("product__category__name")
            .annotate(revenue=Sum(F("unit_price") * F("quantity")), units_sold=Sum("quantity"))
            .order_by("-revenue")
        )
        return [
            {"category": r["product__category__name"] or "Uncategorized", "revenue": float(r["revenue"] or 0), "units_sold": r["units_sold"]}
            for r in rows
        ]

    @staticmethod
    def revenue_trend(days: int = 30):
        since = timezone.now().date() - timedelta(days=days - 1)
        orders = Order.objects.exclude(status=Order.Status.CANCELLED).filter(created_at__date__gte=since)
        trend = []
        today = timezone.now().date()
        for i in range(days - 1, -1, -1):
            day = today - timedelta(days=i)
            day_total = orders.filter(created_at__date=day).aggregate(total=Sum("grand_total"))["total"] or 0
            trend.append({"date": day.isoformat(), "revenue": float(day_total)})
        return trend

    @staticmethod
    def customer_segments():
        totals = User.objects.filter(role="customer").annotate(order_count=Count("orders"))
        new_customers = totals.filter(order_count=1).count()
        returning_customers = totals.filter(order_count__gte=2).count()
        no_orders_yet = totals.filter(order_count=0).count()
        return {
            "new_customers": new_customers,
            "returning_customers": returning_customers,
            "no_orders_yet": no_orders_yet,
        }

    @staticmethod
    def overview(days: int = 30):
        return {
            "top_products": AnalyticsService.top_selling_products(days=days),
            "sales_by_category": AnalyticsService.sales_by_category(days=days),
            "revenue_trend": AnalyticsService.revenue_trend(days=days),
            "customer_segments": AnalyticsService.customer_segments(),
        }
