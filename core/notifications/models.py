from django.db import models
from django.utils.translation import gettext_lazy as _

from core.common.models import BaseModel


class Notification(BaseModel):
    class Status(models.IntegerChoices):
        READY = 1, _("Ready")
        SENDING = 2, _("Sending")
        SENT = 3, _("Sent")
        FAILED = 4, _("Failed")

    class Tags(models.IntegerChoices):
        MENTION = 1, _("Mention")
        INBOX = 2, _("Inbox")
        WORKFLOW = 3, _("Workflow")
        PING = 4, _("Ping")
        REMINDER = 5, _("Reminder")
        COMMENT = 6, _("Comment")

    status = models.IntegerField(db_index=True, choices=Status.choices, default=Status.READY)

    to = models.ForeignKey("users.User", on_delete=models.CASCADE, related_name="%(class)s_received")
    sender = models.ForeignKey(
        "users.User",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="%(class)s_sent",
    )

    sent_at = models.DateTimeField(blank=True, null=True)
    tag = models.IntegerField(choices=Tags.choices, default=Status.READY)

    class Meta:
        abstract = True


class InAppNotification(Notification):
    message = models.CharField(max_length=255)
    is_read = models.BooleanField(default=False)
    is_notified = models.BooleanField(default=False)

    def __str__(self):
        return self.message
