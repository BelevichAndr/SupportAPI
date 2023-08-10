from django.urls import path

from tickets.views import (AllTicketListView, SupportTicketMessageListView,
                           SupportUpdateTicketView, UnsolvedTicketListView,
                           SupportUserMessageCreateView)

app_name = "support_tickets"


urlpatterns = [
    path('unsolved_tickets/', UnsolvedTicketListView.as_view(), name="unsolved_tickets_list"),
    path('all_tickets/', AllTicketListView.as_view(), name="all_ticket_list"),
    path('all_tickets/<int:ticket_pk>/',
         SupportUpdateTicketView.as_view(), name="support_update_ticket"),
    path('all_tickets/<int:ticket_pk>/messages/',
         SupportTicketMessageListView.as_view(), name="support_ticket_messages"),
    path('all_tickets/<int:ticket_pk>/messages/<int:parent_pk>',
         SupportUserMessageCreateView.as_view(), name="support_message_create")
]