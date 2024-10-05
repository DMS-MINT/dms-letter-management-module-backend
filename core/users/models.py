from django.db import models
from django.utils.translation import gettext_lazy as _
from tenant_users.tenants.models import UserProfile as BaseUserProfile

from core.common.models import BaseModel


class User(BaseModel, BaseUserProfile):
    username = None
    first_name = None
    last_name = None

    email = models.EmailField(blank=False, max_length=255, unique=True, verbose_name=_("Email address"))

    otp_secret = models.TextField(editable=False, null=True, blank=True)

    class Meta:
        verbose_name: str = "User"
        verbose_name_plural: str = "Users"

    def __str__(self) -> str:
        return f"{self.email}"
