from django.db import models
from django.utils.translation import gettext_lazy as _

from core.common.models import BaseModel


class OrganizationSetting(BaseModel):
    organization = models.ForeignKey(
        "organizations.Organization",
        on_delete=models.CASCADE,
        related_name="organization_settings",
    )
    auto_ref_number_letters = models.BooleanField(
        default=True,
        verbose_name=_("Auto-generate Reference Numbers for Letters"),
        help_text=_("Enable to automatically generate reference numbers for letters. Disable for manual input."),
    )

    class Meta:
        verbose_name: str = "Organization Setting"
        verbose_name_plural: str = "Organization Settings"

    def __str__(self) -> str:
        return self.organization