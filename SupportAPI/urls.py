from django.conf import settings
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('admin/', admin.site.urls),
    path('tickets/', include("tickets.urls.base", namespace="tickets")),
    path('users/', include("users.urls", namespace="users")),
]

if settings.DEBUG:
    urlpatterns.append(path('__debug__/', include('debug_toolbar.urls')))