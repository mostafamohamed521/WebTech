"""
Serializers for the products app.
"""
from rest_framework import serializers

from apps.brands.serializers import BrandSerializer
from apps.categories.serializers import CategorySerializer
from .models import Product, ProductImage, ProductVariant, ProductSpecification


class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields = ["id", "url", "is_main", "sort_order"]


class ProductVariantSerializer(serializers.ModelSerializer):
    final_price = serializers.SerializerMethodField()

    class Meta:
        model = ProductVariant
        fields = ["id", "color", "storage", "ram", "size", "material", "edition",
                  "price_difference", "stock", "image", "final_price"]

    def get_final_price(self, obj):
        return obj.product.effective_price + obj.price_difference


class ProductSpecificationSerializer(serializers.ModelSerializer):
    key = serializers.CharField(source="specification.key")

    class Meta:
        model = ProductSpecification
        fields = ["key", "value"]


class ProductListSerializer(serializers.ModelSerializer):
    """Lightweight serializer for grid/listing pages."""
    main_image = serializers.SerializerMethodField()
    brand = serializers.CharField(source="brand.name")
    category = serializers.CharField(source="category.name")

    class Meta:
        model = Product
        fields = ["id", "name", "slug", "price", "discount_price", "effective_price",
                  "currency", "brand", "category", "featured", "trending", "in_stock", "main_image"]

    def get_main_image(self, obj):
        main = next((i for i in obj.images.all() if i.is_main), None)
        if main:
            return main.url
        first = obj.images.all()[:1]
        return first[0].url if first else None


class ProductDetailSerializer(serializers.ModelSerializer):
    """Full serializer for the product detail page."""
    brand = BrandSerializer(read_only=True)
    category = CategorySerializer(read_only=True)
    images = ProductImageSerializer(many=True, read_only=True)
    variants = ProductVariantSerializer(many=True, read_only=True)
    specifications = ProductSpecificationSerializer(many=True, read_only=True)

    class Meta:
        model = Product
        fields = [
            "id", "name", "slug", "description", "short_description",
            "brand", "category", "price", "discount_price", "effective_price",
            "currency", "stock", "in_stock", "sku", "warranty",
            "featured", "trending", "images", "variants", "specifications",
            "seo_title", "seo_description", "created_at",
        ]
