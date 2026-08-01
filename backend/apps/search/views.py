"""
Views for the search app.
"""
from django.core.paginator import Paginator
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView

from common.utils.responses import success_response, error_response
from apps.products.serializers import ProductListSerializer
from .services import SearchService


class SearchView(APIView):
    """GET /api/v1/search/?q=...&page=1 — live full-text product search."""
    permission_classes = [AllowAny]

    def get(self, request):
        keyword = request.query_params.get("q", "").strip()
        if not keyword:
            return error_response({"q": ["This field is required."]}, message="Missing search query")

        session_key = request.headers.get("X-Session-Key")
        qs = SearchService.search_products(keyword, user=request.user, session_key=session_key)

        page_size = min(int(request.query_params.get("page_size", 20)), 100)
        paginator = Paginator(qs, page_size)
        page = paginator.get_page(request.query_params.get("page", 1))

        return success_response(
            {
                "keyword": keyword,
                "results": ProductListSerializer(page.object_list, many=True).data,
                "count": paginator.count,
                "num_pages": paginator.num_pages,
                "current_page": page.number,
            },
            message="Search results",
        )


class SuggestionsView(APIView):
    """GET /api/v1/search/suggestions/?q=... — autocomplete."""
    permission_classes = [AllowAny]

    def get(self, request):
        keyword = request.query_params.get("q", "").strip()
        if not keyword:
            return success_response([], message="Suggestions")
        return success_response(SearchService.suggestions(keyword), message="Suggestions")


class RecentSearchesView(APIView):
    """GET /api/v1/search/recent/"""
    permission_classes = [AllowAny]

    def get(self, request):
        session_key = request.headers.get("X-Session-Key")
        return success_response(
            SearchService.recent_searches(user=request.user, session_key=session_key),
            message="Recent searches",
        )


class PopularSearchesView(APIView):
    """GET /api/v1/search/popular/"""
    permission_classes = [AllowAny]

    def get(self, request):
        return success_response(SearchService.popular_searches(), message="Popular searches")
