"""
Serializers for the support app.
"""
from rest_framework import serializers
from .models import SupportTicket, TicketReply


class TicketReplySerializer(serializers.ModelSerializer):
    sender_name = serializers.CharField(source="sender.username", read_only=True)

    class Meta:
        model = TicketReply
        fields = ["id", "sender_name", "message", "is_staff_reply", "created_at"]


class TicketListSerializer(serializers.ModelSerializer):
    customer_email = serializers.CharField(source="user.email", read_only=True)
    reply_count = serializers.IntegerField(source="replies.count", read_only=True)

    class Meta:
        model = SupportTicket
        fields = ["id", "subject", "customer_email", "department", "priority", "status", "created_at", "reply_count"]


class TicketDetailSerializer(serializers.ModelSerializer):
    replies = TicketReplySerializer(many=True, read_only=True)
    customer_email = serializers.CharField(source="user.email", read_only=True)

    class Meta:
        model = SupportTicket
        fields = ["id", "subject", "customer_email", "department", "priority", "status", "order", "replies", "created_at"]


class CreateTicketSerializer(serializers.Serializer):
    subject = serializers.CharField(max_length=255)
    department = serializers.ChoiceField(choices=SupportTicket.Department.choices, default=SupportTicket.Department.GENERAL)
    message = serializers.CharField()
    order_id = serializers.UUIDField(required=False, allow_null=True, default=None)


class AddReplySerializer(serializers.Serializer):
    message = serializers.CharField()


class UpdateTicketSerializer(serializers.Serializer):
    status = serializers.ChoiceField(choices=SupportTicket.Status.choices, required=False)
    priority = serializers.ChoiceField(choices=SupportTicket.Priority.choices, required=False)
