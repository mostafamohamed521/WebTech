from django.urls import path
from .views import ProductReviewListCreateView, ReviewHelpfulView, ReviewDeleteView

app_name = "reviews"

urlpatterns = [
    path("product/<slug:slug>/", ProductReviewListCreateView.as_view(), name="product-reviews"),
    path("<uuid:review_id>/helpful/", ReviewHelpfulView.as_view(), name="helpful"),
    path("<uuid:review_id>/", ReviewDeleteView.as_view(), name="delete"),
]
