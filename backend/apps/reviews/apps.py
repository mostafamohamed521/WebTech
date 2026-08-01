from django.apps import AppConfig


class ReviewsConfig(AppConfig):
    """Configuration for the reviews app.

    Purpose: Product reviews, ratings, review images, helpful votes.
    """
    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.reviews"
    verbose_name = "Reviews"
