from django.contrib import admin

from tickets.models import ClientMessage, SupportSystemMessage, Ticket

admin.site.register(Ticket)
admin.site.register(SupportSystemMessage)
admin.site.register(ClientMessage)
