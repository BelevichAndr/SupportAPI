from django.urls import include, path

from tickets.views import TicketMessageListView

app_name = "tickets"


urlpatterns = [
    path('messages/', TicketMessageListView.as_view(), name="ticket_messages_list"),
    path('my_tickets/', include("tickets.urls.client_urls", namespace="client_tickets")),
    path('support/', include("tickets.urls.support_urls", namespace="support_tickets")),
]
