from celery import shared_task
from celery.utils.log import get_task_logger

from core.common.utils import get_object

from .models import InAppNotification
from .services import notification_send

logger = get_task_logger(__name__)


@shared_task(bind=True)
def notification_send_task(self, notification_id: str):
    notification_instance = get_object(InAppNotification, pk=notification_id)

    try:
        notification_send(notification_instance)

    except InAppNotification.DoesNotExist:
        logger.warning(f"Notification with id {notification_id} does not exist.")

    except Exception as e:
        logger.warning(f"Exception occurred while sending email: {e}")
        # self.retry(exc=e, countdown=5)
