from django.db import models
from django.utils.translation import gettext_lazy as _

from core.common.models import BaseModel


class Contact(BaseModel):
    user = models.ManyToManyField("users.User", related_name="contacts")
    full_name_en = models.CharField(max_length=500, verbose_name=_("Full Name In English"))
    full_name_am = models.CharField(max_length=500, verbose_name=_("Full Name In Amharic"))
    email = models.EmailField(blank=True, null=True, verbose_name=_("Email Address"))
    phone_number = models.CharField(blank=True, null=True, max_length=20, verbose_name=_("Phone Number"))
    address = models.CharField(max_length=255, verbose_name=_("Address"))

    def __str__(self):
        return f"{self.full_name_en} ({self.email or self.phone_number})"

    class Meta:
        unique_together = ("full_name_en", "full_name_am", "address")
