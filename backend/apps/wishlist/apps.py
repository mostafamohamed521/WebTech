from django.apps import AppConfig


class WishlistConfig(AppConfig):
    """Configuration for the wishlist app.

    Purpose: User wishlists and wishlist items.
    """
    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.wishlist"
    verbose_name = "Wishlist"
