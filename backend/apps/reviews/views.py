"""
Views for the reviews app.
"""
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.views import APIView

from common.utils.responses import success_response, error_response
from apps.products.models import Product
from .serializers import ReviewSerializer, CreateReviewSerializer, ProductRatingSummarySerializer
from .services import ReviewService
from .models import Review


class ProductReviewListCreateView(APIView):
    """GET/POST /api/v1/reviews/product/<slug>/"""
    permission_classes = [AllowAny]

    def get_permissions(self):
        if self.request.method == "POST":
            return [IsAuthenticated()]
        return [AllowAny()]

    def get(self, request, slug):
        try:
            product = Product.objects.get(slug=slug, is_deleted=False)
        except Product.DoesNotExist:
            return error_response(message="Product not found", status=404)

        reviews = ReviewService.list_for_product(product)
        summary = ReviewService.rating_summary(product)
        return success_response(
            {
                "summary": ProductRatingSummarySerializer(summary).data,
                "reviews": ReviewSerializer(reviews, many=True, context={"request": request}).data,
            },
            message="Reviews",
        )

    def post(self, request, slug):
        try:
            product = Product.objects.get(slug=slug, is_deleted=False)
        except Product.DoesNotExist:
            return error_response(message="Product not found", status=404)

        serializer = CreateReviewSerializer(data=request.data)
        if not serializer.is_valid():
            return error_response(serializer.errors, message="Invalid review")

        review = ReviewService.create_review(
            request.user, product,
            serializer.validated_data["rating"],
            serializer.validated_data["comment"],
            serializer.validated_data["images"],
        )
        return success_response(ReviewSerializer(review, context={"request": request}).data, message="Review posted", status=201)


class ReviewHelpfulView(APIView):
    """POST /api/v1/reviews/<id>/helpful/ — toggle helpful vote."""
    permission_classes = [IsAuthenticated]

    def post(self, request, review_id):
        try:
            review = Review.objects.get(id=review_id, is_deleted=False)
        except Review.DoesNotExist:
            return error_response(message="Review not found", status=404)
        liked = ReviewService.toggle_helpful(request.user, review)
        return success_response({"liked": liked, "helpful_count": review.helpful_count}, message="Updated")


class ReviewDeleteView(APIView):
    """DELETE /api/v1/reviews/<id>/"""
    permission_classes = [IsAuthenticated]

    def delete(self, request, review_id):
        try:
            review = Review.objects.get(id=review_id, is_deleted=False)
        except Review.DoesNotExist:
            return error_response(message="Review not found", status=404)
        ReviewService.delete_review(request.user, review)
        return success_response(message="Review deleted")
