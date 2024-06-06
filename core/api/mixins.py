from typing import Sequence, Type

from rest_framework.authentication import BaseAuthentication
from rest_framework.permissions import BasePermission, IsAuthenticated


class ApiAuthMixin:
    authentication_classes: Sequence[Type[BaseAuthentication]] = []
    permission_classes: Sequence[Type[BasePermission]] = [IsAuthenticated]
