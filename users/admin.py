from django.contrib import admin

from users.models import ClientUser, SupportSystemUser

admin.site.register(SupportSystemUser)
admin.site.register(ClientUser)