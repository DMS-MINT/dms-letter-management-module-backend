from django.db import models
from django.utils.translation import gettext_lazy as _
from polymorphic.models import PolymorphicModel

from core.common.models import BaseModel


class State(BaseModel):
    name = models.CharField(max_length=255)
    permissions = models.JSONField(default=dict)

    def can_be(self, action):
        return self.permissions.get(action, False)

    def __str__(self):
        return self.name


class Letter(PolymorphicModel, BaseModel):
    state = models.ForeignKey(
        State,
        on_delete=models.CASCADE,
        help_text=_("Select the state of the letter."),
    )
    subject = models.CharField(
        _("Subject"),
        blank=True,
        null=True,
        max_length=255,
        help_text=_("Enter the subject of the letter."),
    )
    content = models.TextField(
        _("Content"),
        blank=True,
        null=True,
        help_text=_("Enter the content of the letter."),
    )

    class Meta:
        verbose_name: str = "Letter"
        verbose_name_plural: str = "Letters"

    def __str__(self) -> str:
        return f"{self.subject} - {self.pk}"


class Internal(Letter):
    class Meta:
        verbose_name: str = "Internal Letter"
        verbose_name_plural: str = "Internal Letters"


class Incoming(Letter):
    class Meta:
        verbose_name: str = "Incoming Letter"
        verbose_name_plural: str = "Incoming Letters"


class Outgoing(Letter):
    delivery_person_name = models.CharField(
        _("Delivery Person Name"),
        blank=True,
        null=True,
        max_length=255,
        help_text=_("Name of the person responsible for delivery."),
    )
    delivery_person_phone = models.CharField(
        _("Delivery Person Phone"),
        blank=True,
        null=True,
        max_length=255,
        help_text=_("Phone number of the delivery person."),
    )
    shipment_id = models.CharField(
        _("Shipment ID"),
        blank=True,
        null=True,
        max_length=255,
        help_text=_("Unique identifier for the shipment."),
    )

    class Meta:
        verbose_name: str = "Outgoing Letter"
        verbose_name_plural: str = "Outgoing Letters"
