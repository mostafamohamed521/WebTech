"""
Serializers for the dashboard app: admin-facing product CRUD, order
management, and aggregated stats.
"""
from django.utils.text import slugify
from rest_framework import serializers

from apps.products.models import Product, ProductImage, ProductVariant
from apps.orders.models import Order


class AdminProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields = ["id", "url", "is_main", "sort_order"]


class AdminProductVariantSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductVariant
        fields = ["id", "color", "storage", "ram", "size", "material", "edition", "price_difference", "stock", "image"]


class AdminProductSerializer(serializers.ModelSerializer):
    """Full read/write serializer for the admin product table + form."""
    images = AdminProductImageSerializer(many=True, read_only=True)
    variants = AdminProductVariantSerializer(many=True, read_only=True)
    brand_name = serializers.CharField(source="brand.name", read_only=True)
    category_name = serializers.CharField(source="category.name", read_only=True)
    slug = serializers.SlugField(required=False, allow_blank=True)
    sku = serializers.CharField(required=False, allow_blank=True)

    class Meta:
        model = Product
        fields = [
            "id", "name", "slug", "description", "short_description",
            "brand", "brand_name", "category", "category_name",
            "price", "discount_price", "cost_price", "currency",
            "stock", "sku", "barcode", "weight", "warranty",
            "featured", "trending", "published",
            "seo_title", "seo_description", "images", "variants", "created_at",
        ]
        read_only_fields = ["id", "created_at"]

    def validate(self, attrs):
        # Auto-generate slug/SKU on create if the admin left them blank —
        # mirrors what a real admin panel does rather than hard-failing.
        if not self.instance:
            name = attrs.get("name", "")
            if not attrs.get("slug"):
                base_slug = slugify(name)[:270] or "product"
                slug = base_slug
                counter = 2
                while Product.objects.filter(slug=slug).exists():
                    slug = f"{base_slug}-{counter}"
                    counter += 1
                attrs["slug"] = slug
            if not attrs.get("sku"):
                attrs["sku"] = f"WT-{slugify(name)[:10].upper() or 'ITEM'}-{Product.objects.count() + 1:04d}"
        return attrs


class AdminOrderListSerializer(serializers.ModelSerializer):
    customer_email = serializers.CharField(source="customer.email", read_only=True)

    class Meta:
        model = Order
        fields = ["id", "order_number", "customer_email", "status", "payment_status", "grand_total", "created_at"]


class UpdateOrderStatusSerializer(serializers.Serializer):
    status = serializers.ChoiceField(choices=Order.Status.choices)
    note = serializers.CharField(required=False, allow_blank=True, default="")


class DashboardStatsSerializer(serializers.Serializer):
    total_revenue = serializers.DecimalField(max_digits=14, decimal_places=2)
    total_orders = serializers.IntegerField()
    total_products = serializers.IntegerField()
    total_customers = serializers.IntegerField()
    orders_by_status = serializers.DictField(child=serializers.IntegerField())
    revenue_last_7_days = serializers.ListField(child=serializers.DictField())
    low_stock_products = serializers.ListField(child=serializers.DictField())
