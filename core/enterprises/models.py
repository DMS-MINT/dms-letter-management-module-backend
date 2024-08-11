from django.db import models
from django.utils.translation import gettext_lazy as _

from core.common.models import BaseModel


def enterprise_directory_path(instance, filename):
    return f"enterprises/{instance.name_en}/logo.png"


class PublicEnterprise(BaseModel):
    name_en = models.CharField(max_length=255, unique=True, verbose_name="Name in English")
    name_am = models.CharField(max_length=255, unique=True, verbose_name="Name in Amharic")
    email = models.EmailField(blank=True, null=True, verbose_name=_("Email Address"))
    phone_number = models.PositiveBigIntegerField(blank=True, null=True, verbose_name=_("Phone Number"))
    address = models.CharField(max_length=255, blank=True, default="Addis Ababa, Ethiopia", verbose_name=_("Address"))
    postal_code = models.PositiveIntegerField(blank=True, null=True, verbose_name=_("Postal Code"))
    logo = models.ImageField(upload_to=enterprise_directory_path, blank=True, null=True, verbose_name="Logo")

    def __str__(self):
        return self.name_en

    class Meta:
        unique_together = ("name_en", "name_am")
