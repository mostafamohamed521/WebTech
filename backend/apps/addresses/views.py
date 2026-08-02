"""
Views for the addresses app.
"""
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView

from common.utils.responses import success_response, error_response
from .models import Address
from .serializers import AddressSerializer
from .services import AddressService


class AddressListCreateView(APIView):
    """GET/POST /api/v1/addresses/"""
    permission_classes = [IsAuthenticated]

    def get(self, request):
        addresses = AddressService.list_for_user(request.user)
        return success_response(AddressSerializer(addresses, many=True).data, message="Addresses")

    def post(self, request):
        serializer = AddressSerializer(data=request.data)
        if not serializer.is_valid():
            return error_response(serializer.errors, message="Invalid address")
        address = AddressService.create(request.user, serializer.validated_data)
        return success_response(AddressSerializer(address).data, message="Address created", status=201)


class AddressDetailView(APIView):
    """GET/PATCH/DELETE /api/v1/addresses/<id>/"""
    permission_classes = [IsAuthenticated]

    def get_object(self, request, pk):
        return Address.objects.get(pk=pk, user=request.user, is_deleted=False)

    def get(self, request, pk):
        try:
            address = self.get_object(request, pk)
        except Address.DoesNotExist:
            return error_response(message="Address not found", status=404)
        return success_response(AddressSerializer(address).data, message="Address")

    def patch(self, request, pk):
        try:
            address = self.get_object(request, pk)
        except Address.DoesNotExist:
            return error_response(message="Address not found", status=404)
        serializer = AddressSerializer(data=request.data, partial=True)
        if not serializer.is_valid():
            return error_response(serializer.errors, message="Invalid address")
        address = AddressService.update(address, serializer.validated_data)
        return success_response(AddressSerializer(address).data, message="Address updated")

    def delete(self, request, pk):
        try:
            address = self.get_object(request, pk)
        except Address.DoesNotExist:
            return error_response(message="Address not found", status=404)
        AddressService.delete(address)
        return success_response(message="Address deleted")
