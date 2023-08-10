from rest_framework.views import APIView

from users.mixins import RegistrationMixin, TokenCreationMixin
from users.models import ClientUser, SupportSystemUser
from users.serializers import (ClientUserRegistrationSerializer,
                               ClientUserSerializer,
                               SupportSystemRegistrationSerializer,
                               SupportSystemSerializer)


class SupportSystemRegistrationView(RegistrationMixin, APIView):
    user_model = SupportSystemUser
    user_response_serializer = SupportSystemSerializer
    serializer_class = SupportSystemRegistrationSerializer



class ClientUserRegistrationView(RegistrationMixin, APIView):
    user_model = ClientUser
    user_response_serializer = ClientUserSerializer
    serializer_class = ClientUserRegistrationSerializer


class SupportSystemAuthTokenView(TokenCreationMixin, APIView):
    user_model = SupportSystemUser


class ClientUserAuthTokenView(TokenCreationMixin, APIView):
    user_model = ClientUser
