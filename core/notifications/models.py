from django.db import models
from django.utils.translation import gettext_lazy as _

from core.common.models import BaseModel


class Tag(BaseModel):
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name


class Notification(BaseModel):
    class Status(models.TextChoices):
        READY = "ready", _("Ready")
        SENDING = "sending", _("Sending")
        SENT = "sent", _("Sent")
        FAILED = "failed", _("Failed")

    status = models.CharField(db_index=True, max_length=50, choices=Status.choices, default=Status.READY)

    to = models.ForeignKey("users.User", on_delete=models.CASCADE, related_name="%(class)s_received")
    sender = models.ForeignKey(
        "users.User",
        on_delete=models.SET_NULL,
        related_name="%(class)s_sent",
        null=True,
        blank=True,
    )

    sent_at = models.DateTimeField(blank=True, null=True)
    tag = models.ManyToManyField(Tag, related_name="%(class)s_tagged_notifications", blank=True)
    action = models.JSONField(default=dict)

    class Meta:
        abstract = True


class InApp(Notification):
    message = models.CharField(max_length=255)
    is_read = models.BooleanField(default=False)
    is_notified = models.BooleanField(default=False)

    def __str__(self):
        return self.message
