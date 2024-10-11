from django.db import models

from core.common.models import BaseModel


class Member(BaseModel):
    user_id = models.UUIDField(unique=True)

    class Meta:
        unique_together = ("user_id",)
        verbose_name = "Member"
        verbose_name_plural = "Members"

    def __str__(self):
        return str(self.user_id)
