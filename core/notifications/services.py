from asgiref.sync import async_to_sync
from channels.layers import get_channel_layer
from django.db import transaction
from django.utils import timezone

from core.api.exceptions import ApplicationError
from core.notifications.serializers import NotificationSerializer
from core.users.models import User

from .models import ChannelType, Notification, NotificationRecipient, Tag


@transaction.atomic()
def notification_create(
    *,
    subject: str,
    tags: list[Tag],
    channels: list[str],
    to: list[str],
    details: dict,
    message: str,
):
    if "in-app" not in channels:
        channels.append(ChannelType.Channels.IN_APP)

    channels = ChannelType.objects.filter(channel_type__in=channels)

    notification_instance = Notification.objects.create(
        status=Notification.Status.READY,
        details=details,
        subject=subject,
        message=message,
    )

    notification_instance.tags.set(tags)
    notification_instance.channels.set(channels)

    notification_recipient_create(notification_instance=notification_instance, to=to)

    return notification_instance


@transaction.atomic()
def notification_recipient_create(*, notification_instance: Notification, to: list[str]):
    users = User.objects.filter(id__in=to)

    if not users.exists():
        raise ValueError("No users found for the provided IDs.")

    NotificationRecipient.objects.bulk_create(
        NotificationRecipient(
            notification=notification_instance,
            user=user,
        )
        for user in users
    )


@transaction.atomic
def notification_send(*, notification_instance: Notification):
    if notification_instance.status != Notification.Status.READY:
        raise ApplicationError(
            f"Cannot send non-ready notifications. Current status is {notification_instance.status}",
        )

    notification_instance.status = Notification.Status.SENDING
    notification_instance.sent_at = timezone.now()
    notification_instance.save()

    recipients = notification_instance.notification_recipients.all()

    for recipient in recipients:
        output_serializer = NotificationSerializer(
            notification_instance,
            context={"user": recipient.user},
        )

        group_name = f"user_{recipient.user.id}"
        channel_layers = get_channel_layer()
        async_to_sync(channel_layers.group_send)(
            group_name,
            {
                "type": "send_notification",
                "message": output_serializer.data,
            },
        )

    notification_instance.status = Notification.Status.SENT

    return notification_instance
