from django.core.exceptions import ValidationError
from django.db import models
from django.utils.translation import gettext_lazy as _
from polymorphic.models import PolymorphicModel

from core.common.models import BaseModel
from core.users.models import BaseUser


class Letter(PolymorphicModel, BaseModel):
    class States(models.IntegerChoices):
        DRAFT = 1, _("Draft")
        SUBMITTED = 2, _("Submitted")
        PUBLISHED = 3, _("Published")
        CLOSED = 4, _("Closed")

    reference_number = models.SlugField(unique=True, verbose_name=_("Reference Number"))

    current_state = models.IntegerField(
        _("States"),
        choices=States.choices,
        help_text=_("Select the current state of the letter."),
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
    owner = models.ForeignKey(
        BaseUser,
        on_delete=models.CASCADE,
        related_name="owned_letters",
    )

    def clean(self):
        if not self.subject or not self.subject.strip():
            raise ValidationError(_("The subject of the letter cannot be empty."))
        if not self.content or not self.content.strip():
            raise ValidationError(_("The content of the letter cannot be empty."))

    def __str__(self) -> str:
        return f"{self.subject} - {self.reference_number}"

    class Meta:
        verbose_name: str = "Letter"
        verbose_name_plural: str = "Letters"
        permissions = (
            # Basic Permissions
            ("can_view_letter", "Can view letter"),
            ("can_update_letter", "Can update letter"),
            ("can_delete_letter", "Can delete letter"),
            ("can_archive_letter", "Can archive letter"),
            # Workflow Permissions
            ("can_share_letter", "Can share letter"),
            ("can_submit_letter", "Can submit letter"),
            ("can_publish_letter", "Can publish letter"),
            ("can_retract_letter", "Can retract letter"),
            ("can_close_letter", "Can close letter"),
            ("can_reopen_letter", "Can reopen letter"),
            # Interaction Permissions
            ("can_comment_letter", "Can comment letter"),
        )


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
