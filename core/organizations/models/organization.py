from django.db import models
from django.utils.translation import gettext_lazy as _
from django_tenants.models import DomainMixin
from tenant_users.tenants.models import TenantBase

from core.common.models import BaseModel


def organization_directory_path(instance, filename):
    return f"organizations/{instance.organization_name_en}/logo.png"


class Organization(TenantBase, BaseModel):
    name_en = models.CharField(max_length=255, verbose_name=_("Organization Name (English)"))
    name_am = models.CharField(max_length=255, verbose_name=_("Organization Name (Amharic)"))

    def __str__(self):
        return f"{self.name_en}"

    class Meta:
        unique_together = ("name_en", "name_am")
        verbose_name = _("Organization")
        verbose_name_plural = _("Organizations")


class Domain(DomainMixin):
    pass
