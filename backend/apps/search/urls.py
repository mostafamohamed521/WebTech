from django.urls import path
from .views import SearchView, SuggestionsView, RecentSearchesView, PopularSearchesView

app_name = "search"

urlpatterns = [
    path("", SearchView.as_view(), name="search"),
    path("suggestions/", SuggestionsView.as_view(), name="suggestions"),
    path("recent/", RecentSearchesView.as_view(), name="recent"),
    path("popular/", PopularSearchesView.as_view(), name="popular"),
]
