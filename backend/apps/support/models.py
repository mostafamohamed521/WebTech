"""
Models for the support app: customer support tickets + replies.
"""
from django.db import models
from common.models import BaseModel
from apps.users.models import User


class SupportTicket(BaseModel):
    class Status(models.TextChoices):
        OPEN = "open", "Open"
        IN_PROGRESS = "in_progress", "In Progress"
        RESOLVED = "resolved", "Resolved"
        CLOSED = "closed", "Closed"

    class Priority(models.TextChoices):
        LOW = "low", "Low"
        NORMAL = "normal", "Normal"
        HIGH = "high", "High"
        URGENT = "urgent", "Urgent"

    class Department(models.TextChoices):
        ORDERS = "orders", "Orders"
        PAYMENTS = "payments", "Payments"
        TECHNICAL = "technical", "Technical"
        GENERAL = "general", "General"

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="support_tickets")
    subject = models.CharField(max_length=255)
    department = models.CharField(max_length=20, choices=Department.choices, default=Department.GENERAL)
    priority = models.CharField(max_length=10, choices=Priority.choices, default=Priority.NORMAL)
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.OPEN, db_index=True)
    order = models.ForeignKey("orders.Order", on_delete=models.SET_NULL, null=True, blank=True, related_name="support_tickets")

    class Meta:
        db_table = "support_tickets"
        ordering = ["-created_at"]

    def __str__(self):
        return f"#{str(self.id)[:8]} — {self.subject}"


class TicketReply(BaseModel):
    ticket = models.ForeignKey(SupportTicket, on_delete=models.CASCADE, related_name="replies")
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name="ticket_replies")
    message = models.TextField()
    is_staff_reply = models.BooleanField(default=False)

    class Meta:
        db_table = "ticket_replies"
        ordering = ["created_at"]
