from django.urls import path
from .views import AddressListCreateView, AddressDetailView

app_name = "addresses"

urlpatterns = [
    path("", AddressListCreateView.as_view(), name="list-create"),
    path("<uuid:pk>/", AddressDetailView.as_view(), name="detail"),
]
