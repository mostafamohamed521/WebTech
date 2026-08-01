from django.contrib import admin
from .models import SearchHistory


@admin.register(SearchHistory)
class SearchHistoryAdmin(admin.ModelAdmin):
    list_display = ("keyword", "user", "results_count", "created_at")
    search_fields = ("keyword",)
