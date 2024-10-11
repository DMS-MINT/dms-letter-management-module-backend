from django.db import models

from core.common.models import BaseModel


class MemberPreference(BaseModel):
    member = models.OneToOneField("members.Member", on_delete=models.CASCADE, related_name="member_preferences")

    class Meta:
        verbose_name: str = "Member Preference"
        verbose_name_plural: str = "Member Preferences"

    def __str__(self) -> str:
        return self.member
