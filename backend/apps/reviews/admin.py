from django.contrib import admin
from .models import Review, ReviewImage, ReviewLike


class ReviewImageInline(admin.TabularInline):
    model = ReviewImage
    extra = 0


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ("product", "user", "rating", "verified_purchase", "helpful_count", "created_at")
    list_filter = ("rating", "verified_purchase")
    search_fields = ("product__name", "user__email")
    inlines = [ReviewImageInline]
