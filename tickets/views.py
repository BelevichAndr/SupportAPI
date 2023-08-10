from rest_framework.generics import (CreateAPIView, ListAPIView,
                                     ListCreateAPIView,
                                     RetrieveUpdateDestroyAPIView,
                                     UpdateAPIView, RetrieveUpdateAPIView)
from rest_framework.response import Response

from tickets.mixins import MessageCreationMixin
from tickets.models import SupportSystemMessage, Ticket, ClientMessage
from tickets.tasks import send_notification_email
from tickets.permissions import IsClient, IsSupportSystemUser, IsClientOwner
from tickets.serializers import (ClientMessageCreateSerializer,
                                 SupportSystemTicketMessageSerializer,
                                 TicketCreationSerializer, TicketSerializer,
                                 TicketSupportUpdateSerializer, SupportMessageCreateSerializer)


class TicketMessageListView(ListAPIView):
    """for tests in base.py"""

    queryset = SupportSystemMessage.objects.filter(parent_message=None).select_related("ticket") \
        .prefetch_related("support_replies__client_replies")
    serializer_class = SupportSystemTicketMessageSerializer


class AllTicketListView(ListAPIView):
    """All tickets for Support"""

    queryset = Ticket.objects.all()
    serializer_class = TicketSerializer
    permission_classes = (IsSupportSystemUser,)


class SupportUpdateTicketView(RetrieveUpdateAPIView):
    """Support can update ticket status"""

    queryset = Ticket.objects.all()
    serializer_class = TicketSupportUpdateSerializer
    permission_classes = (IsSupportSystemUser,)
    lookup_field = "pk"
    lookup_url_kwarg = "ticket_pk"

    def get_serializer_class(self, *args, **kwargs):
        if self.request.method == "GET":
            return TicketSerializer
        return self.serializer_class

    def perform_update(self, serializer):
        instance = serializer.save()
        recipient_email = instance.creator.email
        subject = f"Ticket '{instance.subject}' status update"
        message = f"Status of ticket '{instance.subject}' was updated to '{instance.status}'."
        send_notification_email.delay(subject=subject, message=message, recipient_email=recipient_email)


class UnsolvedTicketListView(ListAPIView):
    """Unsolved tickets for support"""

    queryset = Ticket.objects.filter(status="unsolved")
    serializer_class = TicketSerializer
    permission_classes = (IsSupportSystemUser, )


class SupportTicketMessageListView(ListCreateAPIView):
    """messages for current ticket from ticket_pk and creation first message from support"""

    serializer_class = SupportSystemTicketMessageSerializer
    permission_classes = (IsSupportSystemUser, )

    def get_queryset(self):
        queryset = SupportSystemMessage.objects.filter(parent_message=None).filter(ticket=self.kwargs.get("ticket_pk"))\
            .select_related("ticket").prefetch_related("support_replies__client_replies")
        return queryset

    def perform_create(self, serializer):
        ticket = self.kwargs.get("ticket")
        serializer.save(user=self.request.user, ticket=ticket)

    def get_serializer_class(self, *args, **kwargs):
        if self.request.method == "POST":
            return SupportMessageCreateSerializer
        return self.serializer_class

    def create(self, request, *args, **kwargs):
        ticket_pk = self.kwargs.get("ticket_pk")

        try:
            ticket = Ticket.objects.get(pk=ticket_pk)
        except Ticket.DoesNotExist:
            return Response({"error": f"Ticket with pk {ticket_pk} does not exist"}, status=400)

        if ticket.status != "unsolved":
            return Response({"error": "Ticket status is not 'unsolved'"}, status=400)

        self.kwargs["ticket"] = ticket

        return super().create(request, *args, **kwargs)


class SupportUserMessageCreateView(MessageCreationMixin, CreateAPIView):
    """Create support message"""

    permission_classes = (IsSupportSystemUser, )
    serializer_class = SupportMessageCreateSerializer
    lookup_url_kwarg = "ticket_pk"
    parent_message_model = ClientMessage


class ClientUserTicketsView(ListCreateAPIView):
    """ User tickets list and creation ticket"""

    serializer_class = TicketSerializer
    permission_classes = (IsClient, )

    def get_queryset(self):
        queryset = Ticket.objects.filter(creator=self.request.user)
        return queryset

    def perform_create(self, serializer):
        serializer.save(creator=self.request.user, status="unsolved")

    def get_serializer_class(self, *args, **kwargs):
        if self.request.method == "POST":
            return TicketCreationSerializer
        return self.serializer_class


class ClientUserTicketsDetailView(RetrieveUpdateDestroyAPIView):
    """ User ticket (retr/upd/del)"""

    queryset = Ticket.objects.all()
    serializer_class = TicketCreationSerializer
    permission_classes = (IsClientOwner, )
    lookup_field = "pk"
    lookup_url_kwarg = "ticket_pk"


class ClientUserTicketMessageListView(ListAPIView):
    """Ticket messages (Client)"""

    serializer_class = SupportSystemTicketMessageSerializer
    permission_classes = (IsClientOwner, )

    def get_queryset(self):
        queryset = SupportSystemMessage.objects.filter(parent_message=None).filter(ticket=self.kwargs.get("ticket_pk"))\
            .select_related("ticket").prefetch_related("support_replies__client_replies")
        return queryset


class ClientUserMessageCreateView(MessageCreationMixin, CreateAPIView):
    """Create client message"""

    permission_classes = (IsClientOwner, )
    serializer_class = ClientMessageCreateSerializer
    lookup_url_kwarg = "ticket_pk"
    parent_message_model = SupportSystemMessage
