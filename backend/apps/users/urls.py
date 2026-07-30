"""
URL routes for the users app. Mounted under /api/v1/users/.
"""
from django.urls import path
from .views import MeView

app_name = "users"

urlpatterns = [
    path("me/", MeView.as_view(), name="me"),
]
