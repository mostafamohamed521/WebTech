from django.urls import path
from .views import CartView, CartItemView, CartItemDetailView, ClearCartView

app_name = "cart"

urlpatterns = [
    path("", CartView.as_view(), name="detail"),
    path("items/", CartItemView.as_view(), name="add-item"),
    path("items/<uuid:item_id>/", CartItemDetailView.as_view(), name="item-detail"),
    path("clear/", ClearCartView.as_view(), name="clear"),
]
