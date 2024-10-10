from django.db import models
from django.utils.translation import gettext_lazy as _

from core.common.models import BaseModel


class UserPreference(BaseModel):
    member = models.ForeignKey("user_management.Member", on_delete=models.CASCADE, related_name="member_preference")

    class Meta:
        unique_together = ("member",)
        verbose_name: str = "User Preference"
        verbose_name_plural: str = "User Preferences"

    def __str__(self) -> str:
        return self.member
