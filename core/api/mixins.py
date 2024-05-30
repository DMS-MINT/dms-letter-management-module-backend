from typing import Sequence, Type

from rest_framework.authentication import BaseAuthentication
from rest_framework.permissions import BasePermission, IsAuthenticated
from rest_framework_jwt.authentication import JSONWebTokenAuthentication


class ApiAuthMixin:
    authentication_classes: Sequence[Type[BaseAuthentication]] = [
        JSONWebTokenAuthentication,
    ]
    permission_classes: Sequence[Type[BasePermission]] = [IsAuthenticated]
