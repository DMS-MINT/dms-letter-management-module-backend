from django.db import models
from django.utils.translation import gettext_lazy as _

from core.common.models import BaseModel


class UserSetting(BaseModel):
    member = models.OneToOneField("user_management.Member", on_delete=models.CASCADE, related_name="member_settings")
    is_2fa_enabled = models.BooleanField(default=False)
    is_verified = models.BooleanField(default=False)

    class Meta:
        verbose_name: str = "User Setting"
        verbose_name_plural: str = "User Settings"

    def __str__(self) -> str:
        return self.user
