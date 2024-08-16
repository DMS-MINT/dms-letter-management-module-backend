from django.core.exceptions import ValidationError
from django.db import models
from django.utils.translation import gettext_lazy as _

from core.common.models import BaseModel
from core.letters.models import Letter


def attachment_directory_path(instance, filename):
    if hasattr(instance, "letter"):
        # For LetterAttachment
        department = instance.uploaded_by.department.department_name_en
        letter_ref_no = instance.letter.reference_number
        return f"letters/{department}/letter_{letter_ref_no}/attachments/{filename}"

    # Default fallback path
    return f"fallback/signatures/{filename}"


class Attachment(BaseModel):
    name = models.CharField(max_length=255)
    file_type = models.CharField(max_length=50)
    size = models.IntegerField()
    remote_file_url = models.URLField(max_length=200)
    uploaded_file = models.FileField(upload_to=attachment_directory_path, verbose_name=_("File"))
    uploaded_by = models.ForeignKey(
        "users.User",
        on_delete=models.CASCADE,
        related_name="%(class)s_attachment",
        verbose_name=_("Uploaded By"),
    )
    description = (models.CharField(max_length=255, blank=True, null=True, verbose_name=_("Description")),)

    def clean(self):
        if self.file and self.file_url:
            raise ValidationError("Either upload a file or provide a URL, but not both.")
        if not self.file and not self.file_url:
            raise ValidationError("Either upload a file or provide a URL.")

    def __str__(self):
        return f"Attachment for {self.letter.subject} - {self.file.name}"

    class Meta:
        abstract = True


class LetterAttachment(Attachment):
    letter = models.ForeignKey(
        Letter,
        on_delete=models.CASCADE,
        related_name="letter_attachments",
        verbose_name=_("Letter"),
    )

    class Meta(Attachment.Meta):
        db_table = "letter_attachments"
        verbose_name = _("Letter Attachment")
        verbose_name_plural = _("Letter Attachments")
