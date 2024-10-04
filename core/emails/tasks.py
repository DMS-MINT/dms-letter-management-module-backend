from celery import shared_task

# from celery import task
# from django.core.mail import send_mail
from celery.utils.log import get_task_logger

# from core.emails.email import send_review_email
from .models import Email

logger = get_task_logger(__name__)


def _email_send_failure(self, exc, task_id, args, kwargs, einfo):
    email_id = args[0]
    email = Email.objects.get(id=email_id)

    from .services import email_failed

    email_failed(email)


@shared_task(bind=True, on_failure=_email_send_failure)
def email_send(self, email_id, subject):
    to = email_id

    from .services import email_send

    try:
        email_send(to, subject)
    except Exception as exc:
        # https://docs.celeryq.dev/en/stable/userguide/tasks.html#retrying
        logger.warning(f"Exception occurred while sending email: {exc}")
        self.retry(exc=exc, countdown=5)


@shared_task(bind=True)
def email_send_all(self, email_ids):
    """
    Sends emails to multiple recipients.

    :param email_ids: List of email IDs to send
    """
    for email_id in email_ids:
        try:
            email = Email.objects.get(id=email_id)
            email_send(email)  # Call the existing email_send service
        except Email.DoesNotExist:
            self.retry(exc=Exception(f"Email with ID {email_id} does not exist."), countdown=5)
        except Exception as exc:
            logger.warning(f"Failed to send email ID {email_id}: {exc}")
            self.retry(exc=exc, countdown=5)


# @shared_task(name= 'send_review_email_task')
# def send_review_email_task(name, email, review):
#     subject = "New Review Submission"
#     message = f"Name: {name}\nEmail: {email}\nReview: {review}"
#     try:
#         send_mail(subject, message, 'from@example.com', [email])  # Update 'from@example.com' accordingly
#         return True  # Indicate success
#     except Exception as e:
#         # Log the error or handle it accordingly
#         print(f"Error sending email: {e}")
#         return False
