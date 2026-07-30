from django.urls import path
from .views import WishlistView, WishlistItemDetailView

app_name = "wishlist"

urlpatterns = [
    path("", WishlistView.as_view(), name="list-add"),
    path("<uuid:product_id>/", WishlistItemDetailView.as_view(), name="remove"),
]
