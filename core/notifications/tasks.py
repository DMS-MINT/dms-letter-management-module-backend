from celery import shared_task
from celery.utils.log import get_task_logger
from django.utils import timezone

from core.common.utils import get_object

from .models import Notification
from .services import notification_send

logger = get_task_logger(__name__)


@shared_task(bind=True)
def send_notifications_task(
    self,
    notification_id: str,
    email_id: str = None,
    sms_id: str = None,
):
    try:
        notification_instance = get_object(Notification, pk=notification_id)

        if notification_instance.status == Notification.Status.READY:
            notification_instance.status = Notification.Status.SENDING
            notification_instance.sent_at = timezone.now()
            notification_instance.save()
            notification_send(notification_instance=notification_instance)

    except Notification.DoesNotExist:
        logger.warning(f"Notification with id {notification_id} does not exist.")

    except Exception as e:
        logger.warning(f"Exception occurred while sending email: {e}")
        # self.retry(exc=e, countdown=5)
