from typing import Type, TypeAlias

from django.contrib.auth.hashers import check_password
from rest_framework.response import Response

from users.models import ClientUser, SupportSystemUser
from users.services import (check_password_match, create_access_token,
                            get_user_with_email, check_email_dublication)


Any_User_Model: TypeAlias = Type[ClientUser | SupportSystemUser]


class RegistrationMixin:

    user_model: Any_User_Model = None
    user_response_serializer = None

    def post(self, request):
        serializer = self.serializer_class(data=request.data)

        if serializer.is_valid():
            password1 = serializer.validated_data.get("password")
            password2 = serializer.validated_data.get("password2")
            email = serializer.validated_data.get("email")
            is_match = check_password_match(password1, password2)

            is_dublication = check_email_dublication(user_model=self.user_model, email=email)

            if is_dublication:
                return Response({"error": "User with such email already exists"})

            if is_match:
                serializer.validated_data.pop("password2")
                user = serializer.save()
                response_serializer = self.user_response_serializer(user)
                return Response(response_serializer.data)
            else:
                return Response({"answer": "Password didnt match"})
        return Response(serializer.errors)


class TokenCreationMixin:

    user_model: Any_User_Model = None

    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')
        user = get_user_with_email(email, self.user_model)

        if user is None:
            return Response({'error': 'Invalid email or password'}, status=400)

        if not check_password(password, user.password):
            return Response({'error': 'Invalid email or password'}, status=400)

        access_token = create_access_token(user=user)
        return Response({"token": access_token})
