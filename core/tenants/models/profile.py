from django.db import models
from django.utils.translation import gettext_lazy as _

from core.common.models import BaseModel


def tenant_directory_path(instance, filename):
    return f"tenant/{instance.organization_name_en}/logo.png"


class TenantProfile(BaseModel):
    tenant = models.OneToOneField(
        "tenants.Tenant",
        on_delete=models.CASCADE,
        related_name="tenant_profile",
    )
    bio = models.TextField(blank=True, null=True, verbose_name=_("Description"))
    contact_phone = models.PositiveBigIntegerField(blank=True, null=True, verbose_name=_("Contact Phone"))
    contact_email = models.EmailField(blank=True, null=True, verbose_name=_("Contact Email"))
    address = models.ForeignKey(
        "common.Address",
        on_delete=models.CASCADE,
        related_name="tenant_address",
        verbose_name=_("Address"),
        null=True,
        blank=True,
    )
    postal_code = models.PositiveIntegerField(blank=True, null=True, verbose_name=_("Postal Code"))
    logo = models.ImageField(upload_to=tenant_directory_path, blank=True, null=True, verbose_name="Logo")

    def __str__(self):
        return f"{self.tenant}"

    class Meta:
        verbose_name = _("Tenant Profile")
        verbose_name_plural = _("Tenant Profiles")
