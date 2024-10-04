from django.conf import settings
from django.db import models
from django.utils.translation import gettext_lazy as _

from core.common.models import BaseModel


class UserPreference(BaseModel):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="user_preference")

    class Meta:
        verbose_name: str = "User Preference"
        verbose_name_plural: str = "User Preferences"

    def __str__(self) -> str:
        return self.user
