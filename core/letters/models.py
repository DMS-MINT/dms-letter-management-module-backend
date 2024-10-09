import re

from django.core.exceptions import ValidationError
from django.db import models
from django.utils.translation import gettext_lazy as _
from polymorphic.models import PolymorphicModel
from rest_framework import status as http_status

from core.api.exceptions import APIError
from core.common.models import BaseModel


class Letter(PolymorphicModel, BaseModel):
    class States(models.IntegerChoices):
        DRAFT = 1, _("Draft")
        SUBMITTED = 2, _("Submitted")
        PUBLISHED = 3, _("Published")
        REJECTED = 4, _("Rejected")
        CLOSED = 5, _("Closed")
        TRASHED = 6, _("Trashed")

    class Languages(models.TextChoices):
        ENGLISH = "EN", _("English")
        AMHARIC = "AM", _("Amharic")

    subject = models.CharField(blank=True, null=True, max_length=255)
    body = models.TextField(blank=True, null=True)
    owner = models.ForeignKey("users.User", on_delete=models.CASCADE, related_name="owned_letters")

    reference_number = models.SlugField(unique=True, blank=True, null=True)
    reference_number_am = models.SlugField(unique=True, blank=True, null=True)
    current_state = models.IntegerField(choices=States.choices)
    language = models.CharField(max_length=2, choices=Languages.choices, default=Languages.AMHARIC)

    submitted_at = models.DateTimeField(blank=True, null=True, editable=False)
    published_at = models.DateTimeField(blank=True, null=True, editable=False)

    hidden = models.BooleanField(default=False)

    pdf_version = models.URLField(blank=True, null=True, editable=False)

    class Meta:
        verbose_name: str = "Letter"
        verbose_name_plural: str = "Letters"
        permissions = (
            # Basic Permissions
            ("can_view_letter", "Can view letter"),
            ("can_update_letter", "Can update letter"),
            ("can_archive_letter", "Can archive letter"),
            # Workflow Permissions
            ("can_share_letter", "Can share letter"),
            ("can_submit_letter", "Can submit letter"),
            ("can_publish_letter", "Can publish letter"),
            ("can_reject_letter", "Can reopen letter"),
            ("can_retract_letter", "Can retract letter"),
            ("can_close_letter", "Can close letter"),
            ("can_reopen_letter", "Can reopen letter"),
            # Interaction Permissions
            ("can_comment_letter", "Can comment letter"),
            # Trash and Recover Permissions
            ("can_trash_letter", "Can trash letter"),
            ("can_restore_letter", "Can restore letter"),
            ("can_permanently_delete_letter", "Can permanently delete letter"),
        )

    def clean(self):
        if not self.subject or not self.subject.strip():
            raise ValidationError(_("The subject of the letter cannot be empty."))

        # Skip body validation if the letter is an Incoming letter
        if not isinstance(self, Incoming):
            stripped_body = re.sub("<[^<]+?>", "", self.body or "")
            if not stripped_body.strip():
                raise APIError(
                    error_code="EMPTY_body",
                    status_code=http_status.HTTP_400_BAD_REQUEST,
                    message="Validation error",
                    extra={"body": "The body of the letter cannot be empty."},
                )

        # Check Attachment validation if the letter is an Incoming letter
        if isinstance(self, Incoming):
            if not self.letter_attachments.exists():
                raise APIError(
                    error_code="MISSING_ATTACHMENT",
                    status_code=http_status.HTTP_400_BAD_REQUEST,
                    message="Validation error",
                    extra={"attachment": "The letter must have at least one attachment."},
                )

        if not isinstance(self, Incoming):
            if not self.e_signatures.exists():
                raise APIError(
                    error_code="UNSIGNED_LETTER",
                    status_code=http_status.HTTP_400_BAD_REQUEST,
                    message="Validation error",
                    extra={"e_signature": "The letter must be signed before proceeding."},
                )

    def __str__(self) -> str:
        return f"{self.subject} - {self.reference_number}"


class Internal(Letter):
    class Meta:
        verbose_name: str = "Internal Letter"
        verbose_name_plural: str = "Internal Letters"


class Incoming(Letter):
    class Meta:
        verbose_name: str = "Incoming Letter"
        verbose_name_plural: str = "Incoming Letters"


class Outgoing(Letter):
    delivery_person_name = models.CharField(blank=True, null=True, max_length=255)
    delivery_person_phone = models.CharField(blank=True, null=True, max_length=255)
    shipment_id = models.CharField(blank=True, null=True, max_length=255)

    class Meta:
        verbose_name: str = "Outgoing Letter"
        verbose_name_plural: str = "Outgoing Letters"
