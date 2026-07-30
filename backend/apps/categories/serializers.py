"""
Serializers for the categories app.
"""
from rest_framework import serializers
from .models import Category


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ["id", "name", "slug", "parent", "image", "sort_order"]


class CategoryTreeSerializer(serializers.ModelSerializer):
    children = serializers.SerializerMethodField()

    class Meta:
        model = Category
        fields = ["id", "name", "slug", "image", "sort_order", "children"]

    def get_children(self, obj):
        qs = obj.children.filter(is_active=True, is_deleted=False).order_by("sort_order")
        return CategoryTreeSerializer(qs, many=True).data
