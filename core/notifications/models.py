from django.db import models
from django.utils.translation import gettext_lazy as _

from core.common.models import BaseModel


class Tag(BaseModel):
    name = models.CharField(max_length=255, unique=True)

    def __str__(self):
        return self.name


class ChannelType(BaseModel):
    class Channels(models.TextChoices):
        IN_APP = "in_app", _("In-App")
        EMAIL = "email", _("Email")
        SMS = "sms", _("SMS")

    channel_type = models.CharField(max_length=10, choices=Channels.choices, unique=True)

    def __str__(self):
        return self.get_channel_type_display()


class Notification(BaseModel):
    class Status(models.TextChoices):
        READY = "ready", _("Ready")
        SENDING = "sending", _("Sending")
        SENT = "sent", _("Sent")
        FAILED = "failed", _("Failed")

    status = models.CharField(db_index=True, max_length=50, choices=Status.choices, default=Status.READY)
    channels = models.ManyToManyField(ChannelType, related_name="typed_notifications")

    message = models.CharField(max_length=255, blank=True, null=True)
    subject = models.CharField(max_length=255, blank=True, null=True)
    html_content = models.TextField(blank=True, null=True)

    tags = models.ManyToManyField("Tag", related_name="tagged_notifications", blank=True)
    details = models.JSONField(default=dict)

    sent_at = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return self.subject


class NotificationRecipient(BaseModel):
    notification = models.ForeignKey(Notification, on_delete=models.CASCADE, related_name="notification_recipients")
    user = models.ForeignKey("users.User", on_delete=models.CASCADE, related_name="notifications_received")
    has_read = models.BooleanField(default=False)
    has_notified = models.BooleanField(default=False)

    class Meta:
        unique_together = ("notification", "user")

    def __str__(self):
        return f"{self.user.full_name_en} notifications"
