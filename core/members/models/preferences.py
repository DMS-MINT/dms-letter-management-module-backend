from django.db import models
from django.utils.translation import gettext_lazy as _

from core.common.models import BaseModel


class UserPreference(BaseModel):
    member = models.OneToOneField("members.Member", on_delete=models.CASCADE, related_name="member_preference")

    class Meta:
        verbose_name: str = "Member Preference"
        verbose_name_plural: str = "Member Preferences"

    def __str__(self) -> str:
        return self.member
