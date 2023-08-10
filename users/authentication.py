from datetime import datetime
from typing import Optional, Union

import jwt
from django.conf import settings
from rest_framework import authentication, exceptions

from users.models import BaseUser, ClientUser, SupportSystemUser


class CustomBaseAuthentication(authentication.BaseAuthentication):

    user_model: Union[ClientUser, SupportSystemUser] = None

    def authenticate(self, request) -> Optional[tuple]:

        auth_header = authentication.get_authorization_header(request).split()
        if not auth_header or auth_header[0] != b"Token":
            return None

        if len(auth_header) == 1:
            raise exceptions.AuthenticationFailed("Invalid token header. No credential provided.")

        elif len(auth_header) > 2:
            raise exceptions.AuthenticationFailed("Token string should not contain spaces.")

        try:
            token = auth_header[1].decode("utf-8")
        except UnicodeError:
            raise exceptions.AuthenticationFailed(
                "Invalid token header. Token string should not contain invalid characters.")

        return self.authenticate_credential(token=token)

    def authenticate_credential(self, token):
        try:
            payload = jwt.decode(token, settings.SECRET_KEY, settings.ALGORITHM)
        except jwt.PyJWTError:
            raise exceptions.AuthenticationFailed("invalid authentication. Could not decode token.")

        token_expire = datetime.fromisoformat(payload["expire"])
        if token_expire < datetime.utcnow():
            raise exceptions.AuthenticationFailed("Token expired.")

        try:
            user = self.user_model.objects.get(email=payload["user_email"])
        except self.user_model.DoesNotExist:
            # raise exceptions.AuthenticationFailed("No user matching this token was found.")
            return None
        return user, None


class ClientUserAuthentication(CustomBaseAuthentication):
    user_model = ClientUser


class SupportSystemUserAuthentication(CustomBaseAuthentication):
    user_model = SupportSystemUser
