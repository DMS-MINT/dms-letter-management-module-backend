from django.db import models

from core.notifications.models import Notification


class SMS(Notification):
    message = models.CharField(max_length=255)

    def __str__(self):
        return self.message
