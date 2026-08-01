from django.contrib import admin
from .models import SupportTicket, TicketReply


class TicketReplyInline(admin.TabularInline):
    model = TicketReply
    extra = 0


@admin.register(SupportTicket)
class SupportTicketAdmin(admin.ModelAdmin):
    list_display = ("subject", "user", "department", "priority", "status", "created_at")
    list_filter = ("department", "priority", "status")
    search_fields = ("subject", "user__email")
    inlines = [TicketReplyInline]
