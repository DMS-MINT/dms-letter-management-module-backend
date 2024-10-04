from django.conf import settings
from django.db import models
from django.utils.translation import gettext_lazy as _

from core.common.models import BaseModel


class UserSetting(BaseModel):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="user_settings")
    is_2fa_enabled = models.BooleanField(default=False)
    is_first_time = models.BooleanField(default=False)

    class Meta:
        verbose_name: str = "User Setting"
        verbose_name_plural: str = "User Settings"

    def __str__(self) -> str:
        return self.user
