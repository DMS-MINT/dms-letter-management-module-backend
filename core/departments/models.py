from django.db import models
from django.utils.translation import gettext_lazy as _

from core.common.models import BaseModel


class Department(BaseModel):
    department_name_en = models.CharField(max_length=255, verbose_name=_("Department Name (English)"))
    department_name_am = models.CharField(max_length=255, verbose_name=_("Department Name (Amharic)"))
    abbreviation_en = models.CharField(max_length=3, verbose_name=_("Abbreviation (English)"))
    abbreviation_am = models.CharField(max_length=3, verbose_name=_("Abbreviation (Amharic)"))
    description = models.TextField(blank=True, null=True, verbose_name=_("Description"))
    contact_phone = models.PositiveBigIntegerField(blank=True, null=True, verbose_name=_("Contact Phone"))
    contact_email = models.EmailField(blank=True, null=True, verbose_name=_("Contact Email"))

    def __str__(self):
        return f"{self.department_name_en}"

    class Meta:
        unique_together = ("department_name_en", "department_name_am", "abbreviation_en", "abbreviation_am")
        verbose_name = _("Department")
        verbose_name_plural = _("Departments")
