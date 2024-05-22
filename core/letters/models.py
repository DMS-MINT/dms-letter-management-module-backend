from django.db import models
from django.utils.translation import gettext_lazy as _
from polymorphic.models import PolymorphicModel

from core.common.models import BaseModel


class Letter(PolymorphicModel, BaseModel):
    class LetterStatus(models.IntegerChoices):
        ARCHIVED = 1, _("Archived")
        CANCELLED = 2, _("Cancelled")
        COMPLETED = 3, _("Completed")
        DRAFT = 4, _("Draft")
        DRAFT_PENDING_REVIEW = 5, _("Draft and Pending Review")
        DRAFT_REVIEWED = 6, _("Draft and Reviewed")
        DRAFT_UNDER_REVIEW = 7, _("Draft and Under Review")
        FORWARDED_PENDING_REVIEW = 8, _("Forwarded and Pending Review")
        FORWARDED_REVIEWED = 9, _("Forwarded and Reviewed")
        FORWARDED_UNDER_REVIEW = 10, _("Forwarded and Under Review")
        PENDING_APPROVAL = 11, _("Pending Approval")
        PUBLISHED = 12, _("Published")

    status = models.IntegerField(
        default=LetterStatus.DRAFT,
        choices=LetterStatus.choices,
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
