from django.db import models
from django.utils.translation import gettext_lazy as _

from core.comments.models import BaseModel
from core.users.models import Member


class Signature(BaseModel):
    user = models.OneToOneField(
        Member,
        on_delete=models.CASCADE,
        related_name="e_signature",
        help_text=_("Select the user associated with this signature."),
    )
    e_signature = models.ImageField(
        _("E Signature"),
        unique=True,
        upload_to="letters/signatures/",
        help_text=_("Upload your signature image file."),
    )

    def __str__(self):
        return f"{self.user.full_name}'s signature"

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
