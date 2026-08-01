"""
Service layer for the support app.
"""
from django.db import transaction
from rest_framework.exceptions import PermissionDenied

from apps.orders.models import Order
from .models import SupportTicket, TicketReply


class SupportService:
    @staticmethod
    @transaction.atomic
    def create_ticket(user, subject: str, department: str, message: str, order_id=None) -> SupportTicket:
        order = None
        if order_id:
            order = Order.objects.filter(id=order_id, customer=user).first()

        ticket = SupportTicket.objects.create(user=user, subject=subject, department=department, order=order)
        TicketReply.objects.create(ticket=ticket, sender=user, message=message, is_staff_reply=False)

        from apps.notifications.services import NotificationService
        from apps.notifications.models import Notification
        NotificationService.notify(
            user, title=f"Support ticket #{str(ticket.id)[:8]} created",
            body="Our team will get back to you shortly.",
            type=Notification.Type.SYSTEM, link="/account/support",
        )
        return ticket

    @staticmethod
    def list_for_user(user):
        return SupportTicket.objects.filter(user=user, is_deleted=False)

    @staticmethod
    def get_for_user(user, ticket_id) -> SupportTicket:
        return SupportTicket.objects.prefetch_related("replies").get(id=ticket_id, user=user, is_deleted=False)

    @staticmethod
    def list_all(status: str | None = None):
        qs = SupportTicket.objects.filter(is_deleted=False).select_related("user")
        if status:
            qs = qs.filter(status=status)
        return qs

    @staticmethod
    def get_any(ticket_id) -> SupportTicket:
        return SupportTicket.objects.prefetch_related("replies").get(id=ticket_id, is_deleted=False)

    @staticmethod
    @transaction.atomic
    def add_reply(ticket: SupportTicket, sender, message: str, is_staff: bool) -> TicketReply:
        if not is_staff and ticket.user_id != sender.id:
            raise PermissionDenied("You can only reply to your own tickets.")

        reply = TicketReply.objects.create(ticket=ticket, sender=sender, message=message, is_staff_reply=is_staff)

        if is_staff and ticket.status == SupportTicket.Status.OPEN:
            ticket.status = SupportTicket.Status.IN_PROGRESS
            ticket.save(update_fields=["status"])

        if is_staff:
            from apps.notifications.services import NotificationService
            from apps.notifications.models import Notification
            NotificationService.notify(
                ticket.user, title=f"New reply on ticket #{str(ticket.id)[:8]}",
                body=message[:150], type=Notification.Type.SYSTEM, link="/account/support",
            )
        return reply

    @staticmethod
    def update_ticket(ticket: SupportTicket, data: dict) -> SupportTicket:
        for field, value in data.items():
            setattr(ticket, field, value)
        ticket.save(update_fields=list(data.keys()))
        return ticket
