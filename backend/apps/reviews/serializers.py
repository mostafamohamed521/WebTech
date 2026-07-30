"""
Serializers for the reviews app.
"""
from rest_framework import serializers
from .models import Review, ReviewImage


class ReviewImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReviewImage
        fields = ["id", "url"]


class ReviewSerializer(serializers.ModelSerializer):
    user_name = serializers.CharField(source="user.username", read_only=True)
    user_avatar = serializers.CharField(source="user.avatar", read_only=True)
    images = ReviewImageSerializer(many=True, read_only=True)
    liked_by_me = serializers.SerializerMethodField()

    class Meta:
        model = Review
        fields = [
            "id", "user_name", "user_avatar", "rating", "comment",
            "verified_purchase", "helpful_count", "images", "liked_by_me", "created_at",
        ]

    def get_liked_by_me(self, obj):
        request = self.context.get("request")
        if not request or not request.user.is_authenticated:
            return False
        return obj.likes.filter(user=request.user).exists()


class CreateReviewSerializer(serializers.Serializer):
    rating = serializers.IntegerField(min_value=1, max_value=5)
    comment = serializers.CharField(required=False, allow_blank=True, default="")
    images = serializers.ListField(child=serializers.URLField(), required=False, default=list)


class ProductRatingSummarySerializer(serializers.Serializer):
    average_rating = serializers.FloatField()
    total_reviews = serializers.IntegerField()
    breakdown = serializers.DictField(child=serializers.IntegerField())
