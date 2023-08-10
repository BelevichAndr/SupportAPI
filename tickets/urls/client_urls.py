from django.urls import path

from tickets.views import (ClientUserMessageCreateView,
                           ClientUserTicketMessageListView,
                           ClientUserTicketsDetailView, ClientUserTicketsView)

app_name = "client_tickets"

urlpatterns = [
    path('', ClientUserTicketsView.as_view(), name="user_tickets"),
    path('<int:ticket_pk>/', ClientUserTicketsDetailView.as_view(), name="user_tickets_detail"),
    path('<int:ticket_pk>/messages/',
         ClientUserTicketMessageListView.as_view(), name="current_user_ticket_messages_list"),
    path('<int:ticket_pk>/messages/<int:parent_pk>/',
         ClientUserMessageCreateView.as_view(), name="current_user_message_create"),
]