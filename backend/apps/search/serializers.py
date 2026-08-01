"""
Serializers for the search app.
"""
from rest_framework import serializers
from .models import SearchHistory


class SearchHistorySerializer(serializers.ModelSerializer):
    class Meta:
        model = SearchHistory
        fields = ["keyword", "results_count", "created_at"]


class PopularSearchSerializer(serializers.Serializer):
    keyword = serializers.CharField()
    count = serializers.IntegerField()


class SuggestionSerializer(serializers.Serializer):
    type = serializers.CharField()  # "product" | "category" | "brand"
    label = serializers.CharField()
    slug = serializers.CharField()
