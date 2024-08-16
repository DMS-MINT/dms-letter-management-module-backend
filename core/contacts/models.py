from django.db import models
from django.utils.translation import gettext_lazy as _

from core.common.models import BaseModel


class Contact(BaseModel):
    user = models.ManyToManyField("users.User", related_name="contacts")
    full_name_en = models.CharField(max_length=500, verbose_name=_("Full Name (English)"))
    full_name_am = models.CharField(max_length=500, verbose_name=_("Full Name (Amharic)"))
    email = models.EmailField(blank=True, null=True, verbose_name=_("Email Address"))
    phone_number = models.CharField(blank=True, null=True, max_length=20, verbose_name=_("Phone Number"))
    address = models.ForeignKey(
        "common.Address",
        on_delete=models.CASCADE,
        related_name="contact_address",
        verbose_name=_("Address"),
    )

    def __str__(self):
        return f"{self.full_name_en} ({self.email or self.phone_number})"

    class Meta:
        verbose_name = _("Contact")
        verbose_name_plural = _("Contacts")
        unique_together = ("full_name_en", "full_name_am", "address")
