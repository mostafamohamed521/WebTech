from django.urls import path
from .views import (
    DashboardStatsView, AdminProductListCreateView, AdminProductDetailView,
    AdminOrderListView, AdminOrderStatusView,
)

app_name = "dashboard"

urlpatterns = [
    path("stats/", DashboardStatsView.as_view(), name="stats"),
    path("products/", AdminProductListCreateView.as_view(), name="products"),
    path("products/<uuid:pk>/", AdminProductDetailView.as_view(), name="product-detail"),
    path("orders/", AdminOrderListView.as_view(), name="orders"),
    path("orders/<uuid:pk>/status/", AdminOrderStatusView.as_view(), name="order-status"),
]
