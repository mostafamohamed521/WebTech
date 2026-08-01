"""
Views for the support app.
"""
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView

from common.permissions.roles import IsAdmin
from common.utils.responses import success_response, error_response
from .models import SupportTicket
from .serializers import (
    TicketListSerializer, TicketDetailSerializer, CreateTicketSerializer,
    AddReplySerializer, UpdateTicketSerializer,
)
from .services import SupportService


class TicketListCreateView(APIView):
    """GET/POST /api/v1/support/tickets/ — the current user's own tickets."""
    permission_classes = [IsAuthenticated]

    def get(self, request):
        tickets = SupportService.list_for_user(request.user)
        return success_response(TicketListSerializer(tickets, many=True).data, message="Support tickets")

    def post(self, request):
        serializer = CreateTicketSerializer(data=request.data)
        if not serializer.is_valid():
            return error_response(serializer.errors, message="Invalid ticket data")
        ticket = SupportService.create_ticket(request.user, **serializer.validated_data)
        return success_response(TicketDetailSerializer(ticket).data, message="Ticket created", status=201)


class TicketDetailView(APIView):
    """GET /api/v1/support/tickets/<id>/  |  POST reply"""
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        try:
            ticket = SupportService.get_for_user(request.user, pk)
        except SupportTicket.DoesNotExist:
            return error_response(message="Ticket not found", status=404)
        return success_response(TicketDetailSerializer(ticket).data, message="Ticket detail")

    def post(self, request, pk):
        try:
            ticket = SupportService.get_for_user(request.user, pk)
        except SupportTicket.DoesNotExist:
            return error_response(message="Ticket not found", status=404)
        serializer = AddReplySerializer(data=request.data)
        if not serializer.is_valid():
            return error_response(serializer.errors, message="Invalid reply")
        SupportService.add_reply(ticket, request.user, serializer.validated_data["message"], is_staff=False)
        return success_response(TicketDetailSerializer(ticket).data, message="Reply added")


# ---- Admin ----

class AdminTicketListView(APIView):
    """GET /api/v1/support/admin/tickets/?status=open"""
    permission_classes = [IsAdmin]

    def get(self, request):
        tickets = SupportService.list_all(status=request.query_params.get("status"))
        return success_response(TicketListSerializer(tickets, many=True).data, message="All tickets")


class AdminTicketDetailView(APIView):
    """GET/PATCH /api/v1/support/admin/tickets/<id>/  |  POST reply"""
    permission_classes = [IsAdmin]

    def get(self, request, pk):
        try:
            ticket = SupportService.get_any(pk)
        except SupportTicket.DoesNotExist:
            return error_response(message="Ticket not found", status=404)
        return success_response(TicketDetailSerializer(ticket).data, message="Ticket detail")

    def patch(self, request, pk):
        try:
            ticket = SupportService.get_any(pk)
        except SupportTicket.DoesNotExist:
            return error_response(message="Ticket not found", status=404)
        serializer = UpdateTicketSerializer(data=request.data, partial=True)
        if not serializer.is_valid():
            return error_response(serializer.errors, message="Invalid update")
        ticket = SupportService.update_ticket(ticket, serializer.validated_data)
        return success_response(TicketDetailSerializer(ticket).data, message="Ticket updated")

    def post(self, request, pk):
        try:
            ticket = SupportService.get_any(pk)
        except SupportTicket.DoesNotExist:
            return error_response(message="Ticket not found", status=404)
        serializer = AddReplySerializer(data=request.data)
        if not serializer.is_valid():
            return error_response(serializer.errors, message="Invalid reply")
        SupportService.add_reply(ticket, request.user, serializer.validated_data["message"], is_staff=True)
        return success_response(TicketDetailSerializer(ticket).data, message="Reply added")
