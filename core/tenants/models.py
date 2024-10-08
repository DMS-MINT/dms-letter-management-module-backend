from django.conf import settings
from django.db import models
from django.utils.translation import gettext_lazy as _

from core.common.models import BaseModel


class Tenant(BaseModel):
    name_en = models.CharField(max_length=255, verbose_name=_("Tenant Name (English)"))
    name_am = models.CharField(max_length=255, verbose_name=_("Tenant Name (Amharic)"))

    owner = models.ForeignKey(settings.AUTH_USER_MODEL, related_name="tenant", on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.name_en} ({self.name_am})"

    class Meta:
        unique_together = ("name_en", "owner")
        verbose_name = _("Tenant")
        verbose_name_plural = _("Tenants")


class Domain(BaseModel):
    domain = models.CharField(max_length=253, unique=True, db_index=True)
    tenant = models.ForeignKey(Tenant, db_index=True, related_name="domains", on_delete=models.CASCADE)

    is_primary = models.BooleanField(default=True, db_index=True)

    def __str__(self):
        return f"{self.domain} (Tenant: {self.tenant.name_en})"

    class Meta:
        verbose_name = _("Domain")
        verbose_name_plural = _("Domains")
