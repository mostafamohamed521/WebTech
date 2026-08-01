"""
Serializers for the analytics app.
"""
from rest_framework import serializers


class TopProductSerializer(serializers.Serializer):
    product_id = serializers.CharField()
    name = serializers.CharField()
    sku = serializers.CharField()
    units_sold = serializers.IntegerField()
    revenue = serializers.FloatField()


class CategorySalesSerializer(serializers.Serializer):
    category = serializers.CharField()
    revenue = serializers.FloatField()
    units_sold = serializers.IntegerField()


class RevenueTrendPointSerializer(serializers.Serializer):
    date = serializers.CharField()
    revenue = serializers.FloatField()


class CustomerSegmentsSerializer(serializers.Serializer):
    new_customers = serializers.IntegerField()
    returning_customers = serializers.IntegerField()
    no_orders_yet = serializers.IntegerField()


class AnalyticsOverviewSerializer(serializers.Serializer):
    top_products = TopProductSerializer(many=True)
    sales_by_category = CategorySalesSerializer(many=True)
    revenue_trend = RevenueTrendPointSerializer(many=True)
    customer_segments = CustomerSegmentsSerializer()
