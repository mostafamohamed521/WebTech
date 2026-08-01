from django.urls import path
from .views import TicketListCreateView, TicketDetailView, AdminTicketListView, AdminTicketDetailView

app_name = "support"

urlpatterns = [
    path("tickets/", TicketListCreateView.as_view(), name="tickets"),
    path("tickets/<uuid:pk>/", TicketDetailView.as_view(), name="ticket-detail"),
    path("admin/tickets/", AdminTicketListView.as_view(), name="admin-tickets"),
    path("admin/tickets/<uuid:pk>/", AdminTicketDetailView.as_view(), name="admin-ticket-detail"),
]
