from django.db import models

from core.notifications.models import Notification


class Email(Notification):
    subject = models.CharField(max_length=255)

    html = models.TextField()
    plain_text = models.TextField()

    def __str__(self):
        return self.subject
