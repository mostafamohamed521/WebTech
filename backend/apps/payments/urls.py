from django.urls import path
from .views import OrderPaymentsView

app_name = "payments"

urlpatterns = [
    path("order/<str:order_number>/", OrderPaymentsView.as_view(), name="order-payments"),
]
