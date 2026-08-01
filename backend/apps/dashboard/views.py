"""
Views for the dashboard app — all guarded by IsAdmin.
"""
from django.core.paginator import Paginator
from rest_framework.views import APIView

from common.permissions.roles import IsAdmin
from common.utils.responses import success_response, error_response
from apps.products.models import Product
from apps.orders.models import Order
from .serializers import (
    AdminProductSerializer, AdminOrderListSerializer, UpdateOrderStatusSerializer, DashboardStatsSerializer,
)
from .services import DashboardService


class DashboardStatsView(APIView):
    """GET /api/v1/dashboard/stats/"""
    permission_classes = [IsAdmin]

    def get(self, request):
        stats = DashboardService.get_stats()
        return success_response(DashboardStatsSerializer(stats).data, message="Dashboard stats")


class AdminProductListCreateView(APIView):
    """GET/POST /api/v1/dashboard/products/"""
    permission_classes = [IsAdmin]

    def get(self, request):
        qs = Product.objects.filter(is_deleted=False).select_related("brand", "category").order_by("-created_at")
        search = request.query_params.get("search")
        if search:
            qs = qs.filter(name__icontains=search)

        page_size = min(int(request.query_params.get("page_size", 20)), 100)
        paginator = Paginator(qs, page_size)
        page = paginator.get_page(request.query_params.get("page", 1))

        return success_response(
            {
                "results": AdminProductSerializer(page.object_list, many=True).data,
                "count": paginator.count,
                "num_pages": paginator.num_pages,
                "current_page": page.number,
            },
            message="Products",
        )

    def post(self, request):
        serializer = AdminProductSerializer(data=request.data)
        if not serializer.is_valid():
            return error_response(serializer.errors, message="Invalid product data")
        product = serializer.save()
        return success_response(AdminProductSerializer(product).data, message="Product created", status=201)


class AdminProductDetailView(APIView):
    """GET/PATCH/DELETE /api/v1/dashboard/products/<id>/"""
    permission_classes = [IsAdmin]

    def get_object(self, pk):
        return Product.objects.get(pk=pk, is_deleted=False)

    def get(self, request, pk):
        try:
            product = self.get_object(pk)
        except Product.DoesNotExist:
            return error_response(message="Product not found", status=404)
        return success_response(AdminProductSerializer(product).data, message="Product")

    def patch(self, request, pk):
        try:
            product = self.get_object(pk)
        except Product.DoesNotExist:
            return error_response(message="Product not found", status=404)
        serializer = AdminProductSerializer(product, data=request.data, partial=True)
        if not serializer.is_valid():
            return error_response(serializer.errors, message="Invalid product data")
        product = serializer.save()
        return success_response(AdminProductSerializer(product).data, message="Product updated")

    def delete(self, request, pk):
        try:
            product = self.get_object(pk)
        except Product.DoesNotExist:
            return error_response(message="Product not found", status=404)
        product.soft_delete()
        return success_response(message="Product deleted")


class AdminOrderListView(APIView):
    """GET /api/v1/dashboard/orders/"""
    permission_classes = [IsAdmin]

    def get(self, request):
        qs = Order.objects.select_related("customer").order_by("-created_at")
        status_filter = request.query_params.get("status")
        if status_filter:
            qs = qs.filter(status=status_filter)

        page_size = min(int(request.query_params.get("page_size", 20)), 100)
        paginator = Paginator(qs, page_size)
        page = paginator.get_page(request.query_params.get("page", 1))

        return success_response(
            {
                "results": AdminOrderListSerializer(page.object_list, many=True).data,
                "count": paginator.count,
                "num_pages": paginator.num_pages,
                "current_page": page.number,
            },
            message="Orders",
        )


class AdminOrderStatusView(APIView):
    """PATCH /api/v1/dashboard/orders/<id>/status/"""
    permission_classes = [IsAdmin]

    def patch(self, request, pk):
        try:
            order = Order.objects.get(pk=pk)
        except Order.DoesNotExist:
            return error_response(message="Order not found", status=404)
        serializer = UpdateOrderStatusSerializer(data=request.data)
        if not serializer.is_valid():
            return error_response(serializer.errors, message="Invalid status")
        order = DashboardService.update_order_status(order, **serializer.validated_data)
        return success_response(AdminOrderListSerializer(order).data, message="Order status updated")
