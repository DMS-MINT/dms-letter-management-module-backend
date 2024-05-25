from django.db import models
from django.utils.translation import gettext_lazy as _

from core.common.models import BaseModel
from core.letters.models import Letter
from core.users.models import BaseUser


class Participant(BaseModel):

    class Roles(models.IntegerChoices):
        BCC = 1, _("Blind Carbon Copy Recipient")
        CC = 2, _("Carbon Copy Recipient")
        DRAFTER = 3, _("Drafter")
        FORWARDED_RECIPIENT = 4, _("Forwarded Recipient")
        FORWARDER = 5, _("Forwarder")
        RECIPIENT = 6, _("Recipient")
        DRAFT_REVIEWER = 7, _("Draft Reviewer")
        SENDER = 8, _("Sender")
        WORKFLOW_MANAGER = 9, _("Workflow Manager")

    user = models.ForeignKey(
        BaseUser,
        on_delete=models.CASCADE,
        related_name="participates_in",
        help_text=_("Select the user associated with this participant."),
    )
    role = models.IntegerField(
        _("Role"),
        choices=Roles.choices,
        help_text=_("Select the role of this participant."),
    )
    letter = models.ForeignKey(
        Letter,
        on_delete=models.CASCADE,
        related_name="letter_participants",
        help_text=_("Select the letter associated with this participant."),
    )
    is_reading = models.BooleanField(default=False, editable=False)
    last_read_at = models.DateTimeField(blank=True, null=True, editable=False)
    message = models.TextField(
        _("Message"),
        blank=True,
        null=True,
        help_text=_("Enter a message for the participant."),
    )
    signature_image = models.ImageField(
        _("Signature Image"),
        upload_to="signatures/",
        blank=True,
        null=True,
        help_text=_("Upload a signature image for the participant."),
    )

    class Meta:
        verbose_name: str = _("Participant")
        verbose_name_plural: str = _("Participants")
