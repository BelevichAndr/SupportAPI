from datetime import datetime, timedelta
from typing import Optional, TypeAlias, Type

import jwt
from django.conf import settings

from users.models import ClientUser, SupportSystemUser


Any_User_Model: TypeAlias = Type[ClientUser | SupportSystemUser]
Any_User: TypeAlias = ClientUser | SupportSystemUser


def check_password_match(password1: str, password2: str) -> bool:
    return password1 == password2


def get_user_with_email(email: str, user_model: Any_User_Model) -> Optional[Any_User]:

    try:
        user = user_model.objects.get(email=email)
    except user_model.DoesNotExist:
        return None

    return user


def create_access_token(user: ClientUser | SupportSystemUser):
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    expire = (datetime.utcnow() + access_token_expires).isoformat()

    data = {
        "user_email": user.email,
        "token_type": "Token",
        "expire": expire,
    }
    encoded_jwt = jwt.encode(data, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt


def check_email_dublication(user_model: Any_User_Model, email: str) -> bool:
    """checks for the presence of a parallel user account with the same email
    for Client check Support
    for Support check Client """

    parallel_user_model = ClientUser if user_model == SupportSystemUser else SupportSystemUser

    user = get_user_with_email(user_model=parallel_user_model, email=email)
    return bool(user)
