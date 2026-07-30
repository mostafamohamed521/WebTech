"""
Models for the products app: core catalog (products, images, variants, specs).
"""
from django.db import models
from common.models import BaseModel
from apps.brands.models import Brand
from apps.categories.models import Category


class Product(BaseModel):
    name = models.CharField(max_length=255, db_index=True)
    slug = models.SlugField(max_length=280, unique=True, db_index=True)
    description = models.TextField(blank=True)
    short_description = models.CharField(max_length=500, blank=True)

    brand = models.ForeignKey(Brand, on_delete=models.PROTECT, related_name="products")
    category = models.ForeignKey(Category, on_delete=models.PROTECT, related_name="products")

    price = models.DecimalField(max_digits=12, decimal_places=2)
    discount_price = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    cost_price = models.DecimalField(max_digits=12, decimal_places=2, null=True, blank=True)
    currency = models.CharField(max_length=3, default="EGP")

    stock = models.PositiveIntegerField(default=0)
    sku = models.CharField(max_length=64, unique=True, db_index=True)
    barcode = models.CharField(max_length=64, blank=True, db_index=True)
    weight = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True)
    warranty = models.CharField(max_length=100, blank=True)

    featured = models.BooleanField(default=False, db_index=True)
    trending = models.BooleanField(default=False, db_index=True)
    published = models.BooleanField(default=True, db_index=True)

    seo_title = models.CharField(max_length=255, blank=True)
    seo_description = models.CharField(max_length=500, blank=True)

    class Meta:
        db_table = "products"
        indexes = [
            models.Index(fields=["slug"]),
            models.Index(fields=["sku"]),
            models.Index(fields=["name"]),
            models.Index(fields=["category", "brand"]),
            models.Index(fields=["featured", "trending", "published"]),
        ]
        ordering = ["-created_at"]

    def __str__(self):
        return self.name

    @property
    def in_stock(self):
        return self.stock > 0

    @property
    def effective_price(self):
        return self.discount_price if self.discount_price else self.price


class ProductImage(BaseModel):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="images")
    url = models.URLField()
    is_main = models.BooleanField(default=False)
    sort_order = models.PositiveIntegerField(default=0)

    class Meta:
        db_table = "product_images"
        ordering = ["sort_order"]


class ProductVideo(BaseModel):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="videos")
    url = models.URLField()

    class Meta:
        db_table = "product_videos"


class ProductVariant(BaseModel):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="variants")
    color = models.CharField(max_length=50, blank=True)
    storage = models.CharField(max_length=50, blank=True)
    ram = models.CharField(max_length=50, blank=True)
    size = models.CharField(max_length=50, blank=True)
    material = models.CharField(max_length=50, blank=True)
    edition = models.CharField(max_length=100, blank=True)
    price_difference = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    stock = models.PositiveIntegerField(default=0)
    image = models.URLField(blank=True)

    class Meta:
        db_table = "product_variants"

    def __str__(self):
        bits = [self.color, self.storage, self.ram, self.size]
        return " / ".join(b for b in bits if b) or f"Variant<{self.id}>"


class Specification(BaseModel):
    """Spec dictionary key, e.g. CPU, GPU, RAM, Display, Battery..."""
    key = models.CharField(max_length=100, unique=True)

    class Meta:
        db_table = "specifications"

    def __str__(self):
        return self.key


class ProductSpecification(BaseModel):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name="specifications")
    specification = models.ForeignKey(Specification, on_delete=models.CASCADE)
    value = models.CharField(max_length=255)

    class Meta:
        db_table = "product_specifications"
        unique_together = ("product", "specification")
