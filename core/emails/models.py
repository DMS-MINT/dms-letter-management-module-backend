from django.db import models
from django.utils.translation import gettext_lazy as _

from core.common.models import BaseModel


class Email(BaseModel):
    class Status(models.TextChoices):
        READY = "READY", _("Ready")
        SENDING = "SENDING", _("Sending")
        SENT = "SENT", _("Sent")
        FAILED = "FAILED", _("Failed")

    status = models.CharField(max_length=255, db_index=True, choices=Status.choices, default=Status.READY)

    to = models.OneToOneField("users.User", on_delete=models.CASCADE, related_name="email_received")
    subject = models.CharField(max_length=255)

    html = models.TextField()
    plain_text = models.TextField()

    sent_at = models.DateTimeField(blank=True, null=True)
