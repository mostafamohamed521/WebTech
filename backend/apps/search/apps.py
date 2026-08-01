from django.apps import AppConfig


class SearchConfig(AppConfig):
    """Configuration for the search app.

    Purpose: Full text search, autocomplete, search history.
    """
    default_auto_field = "django.db.models.BigAutoField"
    name = "apps.search"
    verbose_name = "Search"
