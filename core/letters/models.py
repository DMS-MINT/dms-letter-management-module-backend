from django.db import models
from django.utils.translation import gettext_lazy as _
from polymorphic.models import PolymorphicModel

from core.common.models import BaseModel
from core.permissions.models import Permission


class State(BaseModel):
    name = models.CharField(max_length=255)
    actions = models.ManyToManyField(Permission)

    def __str__(self):
        return self.name

    def can(self, action):
        return self.actions.filter(name=action).exists()

    class Meta:
        verbose_name: str = _("State")
        verbose_name_plural: str = _("States")


class Letter(PolymorphicModel, BaseModel):
    reference_number = models.SlugField(verbose_name=_("Reference Number"), blank=True, null=True)
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
