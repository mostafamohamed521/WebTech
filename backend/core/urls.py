"""
Root URL configuration for WEBTECH.

All API routes are versioned under /api/v1/.
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from drf_spectacular.views import SpectacularAPIView, SpectacularSwaggerView, SpectacularRedocView

API_V1 = [
    path("authentication/", include("apps.authentication.urls")),
    path("users/", include("apps.users.urls")),
    path("addresses/", include("apps.addresses.urls")),
    path("categories/", include("apps.categories.urls")),
    path("brands/", include("apps.brands.urls")),
    path("products/", include("apps.products.urls")),
    path("inventory/", include("apps.inventory.urls")),
    path("cart/", include("apps.cart.urls")),
    path("wishlist/", include("apps.wishlist.urls")),
    path("orders/", include("apps.orders.urls")),
    path("payments/", include("apps.payments.urls")),
    path("reviews/", include("apps.reviews.urls")),
    path("coupons/", include("apps.coupons.urls")),
    path("notifications/", include("apps.notifications.urls")),
    path("analytics/", include("apps.analytics.urls")),
    path("dashboard/", include("apps.dashboard.urls")),
    path("search/", include("apps.search.urls")),
    path("support/", include("apps.support.urls")),
]

urlpatterns = [
    path("admin/", admin.site.urls),
    path("api/v1/", include(API_V1)),

    # API docs
    path("api/schema/", SpectacularAPIView.as_view(), name="schema"),
    path("api/docs/", SpectacularSwaggerView.as_view(url_name="schema"), name="swagger-ui"),
    path("api/redoc/", SpectacularRedocView.as_view(url_name="schema"), name="redoc"),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
