from django.db import models
from django.utils.translation import gettext_lazy as _

from core.common.models import BaseModel


def organization_directory_path(instance, filename):
    return f"organizations/{instance.organization_name_en}/logo.png"


class OrganizationProfile(BaseModel):
    organization = models.ForeignKey(
        "organizations.Organization",
        on_delete=models.CASCADE,
        related_name="organization_profile",
    )
    bio = models.TextField(blank=True, null=True, verbose_name=_("Description"))
    contact_phone = models.PositiveBigIntegerField(blank=True, null=True, verbose_name=_("Contact Phone"))
    contact_email = models.EmailField(blank=True, null=True, verbose_name=_("Contact Email"))
    address = models.ForeignKey(
        "common.Address",
        on_delete=models.CASCADE,
        related_name="organization_address",
        verbose_name=_("Address"),
        null=True,
        blank=True,
    )
    postal_code = models.PositiveIntegerField(blank=True, null=True, verbose_name=_("Postal Code"))
    logo = models.ImageField(upload_to=organization_directory_path, blank=True, null=True, verbose_name="Logo")

    def __str__(self):
        return f"{self.name_en}"

    class Meta:
        verbose_name = _("Organization Profile")
        verbose_name_plural = _("Organization Profiles")
