from django.apps import AppConfig


class CategoriesConfig(AppConfig):
    """Configuration for the categories app.

    Purpose: Product categories and sub-categories tree.
    """
    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.categories"
    verbose_name = "Categories"
