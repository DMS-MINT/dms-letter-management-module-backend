from django.db import transaction
from django.utils import timezone

from core.api.exceptions import ApplicationError
from core.users.models import User

from .models import InAppNotification, Notification


@transaction.atomic
def notification_send(notification_instance: InAppNotification):
    if notification_instance.status != Notification.Status.SENDING:
        raise ApplicationError(f"Cannot send non-ready notifications. Current status is {notification_instance.status}")

    # CALL THE CHANNEL FROM HERE
