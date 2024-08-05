from django.db import models

from core.common.models import BaseModel


class Department(BaseModel):
    name_en = models.CharField(max_length=255)
    name_am = models.CharField(max_length=255)
    abbreviation_en = models.CharField(max_length=3)
    abbreviation_am = models.CharField(max_length=3)
    description = models.TextField(blank=True, null=True)
    contact_phone = models.PositiveBigIntegerField(blank=True, null=True)
    contact_email = models.EmailField(blank=True, null=True)

    def __str__(self):
        return f"{self.name_en}"

    class Meta:
        unique_together = ("name_en", "name_am", "abbreviation_en", "abbreviation_am")
