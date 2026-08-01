from django.urls import path
from .views import CheckoutView, OrderListView, OrderDetailView

app_name = "orders"

urlpatterns = [
    path("checkout/", CheckoutView.as_view(), name="checkout"),
    path("", OrderListView.as_view(), name="list"),
    path("<str:order_number>/", OrderDetailView.as_view(), name="detail"),
]
