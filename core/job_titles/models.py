from django.db import models
from django.utils.translation import gettext_lazy as _

from core.common.models import BaseModel


class JobTitle(BaseModel):
    title_en = models.CharField(max_length=255, verbose_name=_("Job Title (English)"))
    title_am = models.CharField(max_length=255, verbose_name=_("Job Title (Amharic)"))

    def __str__(self):
        return f"{self.title_en}"

    class Meta:
        unique_together = ("title_en", "title_am")
