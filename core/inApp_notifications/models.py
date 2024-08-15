from django.db import models

from core.notifications.models import BaseNotification


class InAppNotification(BaseNotification):
    message = models.CharField(max_length=255)
    is_read = models.BooleanField(default=False)
    is_notified = models.BooleanField(default=False)

    def __str__(self):
        return self.message
