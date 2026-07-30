from django.urls import path
from .views import BrandListView

app_name = "brands"

urlpatterns = [
    path("", BrandListView.as_view(), name="list"),
]
