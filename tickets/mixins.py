from typing import Union

from rest_framework.response import Response

from tickets.models import Ticket, ClientMessage, SupportSystemMessage


class MessageCreationMixin:
    """ Mixin for creation message"""

    parent_message_model: ClientMessage | SupportSystemMessage = None

    def post(self, request, *args, **kwargs):
        parent_pk = self.kwargs.get("parent_pk")
        ticket_pk = self.kwargs.get("ticket_pk")

        try:
            ticket = Ticket.objects.get(pk=ticket_pk)
        except Ticket.DoesNotExist:
            return Response({"error": f"Ticket with pk {ticket_pk} does not exist"}, status=400)

        try:
            parent_message = self.parent_message_model.objects.get(pk=parent_pk)
        except self.parent_message_model.DoesNotExist:
            return Response({"error": f"Message with pk {parent_pk} does not exist"}, status=400)

        # if parent_message.ticket.creator != request.user:
        #     return Response({"error": "You are not allowed to add reply to this message"}, status=403)

        if parent_message.ticket != ticket:
            return Response({"error": "You are not allowed to add reply to this message"}, status=403)

        if ticket.status != "unsolved":
            return Response({"error": "Ticket status is not 'unsolved'"}, status=400)

        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save(parent_message=parent_message, user=request.user, ticket=ticket)
        else:
            return Response({'error': 'Serializer is not valid'}, status=400)

        return Response(serializer.data, status=201)