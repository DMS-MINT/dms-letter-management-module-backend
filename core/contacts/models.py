from django.conf import settings
from django.db import models
from django.utils.translation import gettext_lazy as _

from core.common.models import BaseModel


def profile_picture_directory_path(instance, filename):
    return f"contacts/{instance.id}/{filename}"


class Contact(BaseModel):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="contacts")
    full_name_en = models.CharField(max_length=500, verbose_name=_("Full Name"))
    full_name_am = models.CharField(max_length=500, verbose_name=_("Full Name"))
    email = models.EmailField(blank=True, null=True, verbose_name=_("Email Address"))
    phone_number = models.CharField(blank=True, null=True, max_length=20, verbose_name=_("Phone Number"))
    address = models.CharField(max_length=255, verbose_name=_("Address"))
    profile_picture = models.ImageField(
        upload_to=profile_picture_directory_path,
        blank=True,
        null=True,
        verbose_name=_("Profile Picture"),
    )

    def __str__(self):
        return f"{self.full_name_en} ({self.email or self.phone_number})"

    class Meta:
        unique_together = ("full_name_en", "full_name_am", "address")
        indexes = [models.Index(fields=["user"])]
