"""
Views for the products app.
"""
from django.core.paginator import Paginator
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView

from common.utils.responses import success_response, error_response
from .serializers import ProductListSerializer, ProductDetailSerializer
from .services import ProductService


class ProductListView(APIView):
    """
    GET /api/v1/products/
    Query params: category, brand, search, min_price, max_price,
                  featured, trending, ordering, page, page_size
    """
    permission_classes = [AllowAny]

    def get(self, request):
        params = request.query_params

        def as_bool(v):
            return v.lower() in ("1", "true", "yes") if v is not None else None

        qs = ProductService.list_products(
            category=params.get("category"),
            brand=params.get("brand"),
            search=params.get("search"),
            min_price=params.get("min_price"),
            max_price=params.get("max_price"),
            featured=as_bool(params.get("featured")),
            trending=as_bool(params.get("trending")),
            ordering=params.get("ordering"),
        )

        page_size = min(int(params.get("page_size", 20)), 100)
        paginator = Paginator(qs, page_size)
        page = paginator.get_page(params.get("page", 1))

        return success_response(
            {
                "results": ProductListSerializer(page.object_list, many=True).data,
                "count": paginator.count,
                "num_pages": paginator.num_pages,
                "current_page": page.number,
            },
            message="Products fetched",
        )


class ProductDetailView(APIView):
    """GET /api/v1/products/<slug>/"""
    permission_classes = [AllowAny]

    def get(self, request, slug):
        try:
            product = ProductService.get_by_slug(slug)
        except Exception:
            return error_response(message="Product not found", status=404)

        data = ProductDetailSerializer(product).data
        data["related_products"] = ProductListSerializer(
            ProductService.related_products(product), many=True
        ).data
        return success_response(data, message="Product detail")
