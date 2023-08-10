from django.urls import path

from users.views import (ClientUserAuthTokenView, ClientUserRegistrationView,
                         SupportSystemAuthTokenView,
                         SupportSystemRegistrationView)

app_name = "users"


urlpatterns = [
    path('support/register', SupportSystemRegistrationView.as_view(), name="support_register"),
    path('support/get_token', SupportSystemAuthTokenView.as_view(), name="support_auth_token"),
    path('client/register', ClientUserRegistrationView.as_view(), name="client_register"),
    path('client/get_token', ClientUserAuthTokenView.as_view(), name="client_auth_token"),
]