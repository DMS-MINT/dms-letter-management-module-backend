from django.db import models
from django.utils.translation import gettext_lazy as _

from core.common.models import BaseModel
from core.letters.models import Letter
from core.users.models import Member


class Attachment(BaseModel):
    letter = models.ForeignKey(
        Letter,
        on_delete=models.CASCADE,
        related_name="attachments",
        verbose_name=_("Letter"),
        help_text=_("The letter to which this attachment belongs."),
    )
    file = models.FileField(
        upload_to="letters/attachments/",
        verbose_name=_("File"),
        help_text=_("Upload the attachment file."),
    )
    description = (
        models.CharField(
            max_length=255,
            blank=True,
            null=True,
            verbose_name=_("Description"),
            help_text=_("A brief description of the attachment."),
        ),
    )
    uploaded_by = models.ForeignKey(
        Member,
        on_delete=models.CASCADE,
        related_name="files",
        verbose_name=_("Uploaded By"),
        help_text=_("The person who uploaded the attachment."),
    )

    def __str__(self):
        return f"Attachment for {self.letter.subject} - {self.file.name}"

    class Meta:
        verbose_name = _("Attachment")
        verbose_name_plural = _("Attachments")
