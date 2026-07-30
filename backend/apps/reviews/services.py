"""
Service layer for the reviews app: create/verify-purchase, helpful
votes, rating aggregation.
"""
from django.db import transaction
from django.db.models import Avg, Count
from rest_framework.exceptions import ValidationError, PermissionDenied

from apps.orders.models import OrderItem
from .models import Review, ReviewImage, ReviewLike


class ReviewService:
    @staticmethod
    def _has_purchased(user, product) -> bool:
        return OrderItem.objects.filter(
            order__customer=user, product=product, order__status__in=["confirmed", "processing", "shipped", "delivered"]
        ).exists()

    @staticmethod
    @transaction.atomic
    def create_review(user, product, rating: int, comment: str, image_urls: list[str]) -> Review:
        if Review.objects.filter(user=user, product=product).exists():
            raise ValidationError({"review": ["You have already reviewed this product."]})

        review = Review.objects.create(
            user=user, product=product, rating=rating, comment=comment,
            verified_purchase=ReviewService._has_purchased(user, product),
        )
        for url in image_urls:
            ReviewImage.objects.create(review=review, url=url)
        return review

    @staticmethod
    def list_for_product(product, ordering="-helpful_count"):
        return Review.objects.filter(product=product, is_deleted=False).select_related("user").prefetch_related("images", "likes").order_by(ordering)

    @staticmethod
    def rating_summary(product) -> dict:
        reviews = Review.objects.filter(product=product, is_deleted=False)
        agg = reviews.aggregate(average=Avg("rating"), total=Count("id"))
        breakdown = {str(i): 0 for i in range(1, 6)}
        for row in reviews.values("rating").annotate(count=Count("id")):
            breakdown[str(row["rating"])] = row["count"]
        return {
            "average_rating": round(agg["average"] or 0, 1),
            "total_reviews": agg["total"] or 0,
            "breakdown": breakdown,
        }

    @staticmethod
    @transaction.atomic
    def toggle_helpful(user, review: Review) -> bool:
        like, created = ReviewLike.objects.get_or_create(review=review, user=user)
        if not created:
            like.delete()
            Review.objects.filter(id=review.id).update(helpful_count=max(0, review.helpful_count - 1))
            return False
        Review.objects.filter(id=review.id).update(helpful_count=review.helpful_count + 1)
        return True

    @staticmethod
    def delete_review(user, review: Review):
        if review.user_id != user.id:
            raise PermissionDenied("You can only delete your own review.")
        review.soft_delete()
