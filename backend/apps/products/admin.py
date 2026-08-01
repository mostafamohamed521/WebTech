from django.contrib import admin
from .models import Product, ProductImage, ProductVideo, ProductVariant, Specification, ProductSpecification


class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1


class ProductVariantInline(admin.TabularInline):
    model = ProductVariant
    extra = 1


class ProductSpecificationInline(admin.TabularInline):
    model = ProductSpecification
    extra = 1


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("name", "sku", "brand", "category", "price", "stock", "featured", "trending", "published")
    list_filter = ("brand", "category", "featured", "trending", "published")
    search_fields = ("name", "sku", "barcode", "slug")
    prepopulated_fields = {"slug": ("name",)}
    inlines = [ProductImageInline, ProductVariantInline, ProductSpecificationInline]


@admin.register(Specification)
class SpecificationAdmin(admin.ModelAdmin):
    search_fields = ("key",)
