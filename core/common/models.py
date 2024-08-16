import uuid

from django.db import models
from django.utils.translation import gettext_lazy as _


class BaseModel(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_at = models.DateTimeField(db_index=True, auto_now_add=True, editable=False)
    updated_at = models.DateTimeField(auto_now=True, editable=False)

    class Meta:
        abstract = True


class Address(BaseModel):
    city_en = models.CharField(max_length=100, verbose_name=_("City (English)"))
    city_am = models.CharField(max_length=100, verbose_name=_("City (Amharic)"))

    class Meta:
        verbose_name = _("Address")
        verbose_name_plural = _("Addresses")
        unique_together = ("city_en", "city_am")

    def __str__(self):
        return f"{self.city_en}"
