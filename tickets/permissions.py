from rest_framework.permissions import BasePermission

from tickets.models import Ticket
from users.models import ClientUser, SupportSystemUser


class IsSupportSystemUser(BasePermission):
    def has_permission(self, request, view):
        return isinstance(request.user, SupportSystemUser)


class IsClient(BasePermission):
    def has_permission(self, request, view):
        return isinstance(request.user, ClientUser)


class IsClientOwner(BasePermission):

    def has_permission(self, request, view):
        ticket_id = view.kwargs.get('ticket_pk')
        try:
            ticket = Ticket.objects.get(pk=ticket_id)
            return ticket.creator == request.user
        except Ticket.DoesNotExist:
            return False

    # def has_object_permission(self, request, view, obj):
    #     return obj.creator == request.user and isinstance(request.user, ClientUser)
