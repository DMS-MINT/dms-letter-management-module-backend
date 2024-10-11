import random

from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.db import transaction
from django.db.models.query import QuerySet

from core.api.exceptions import ApplicationError

from .models import Email


@transaction.atomic
def email_failed(email: Email) -> Email:
    if email.status != Email.Status.SENDING:
        raise ApplicationError(
            "INVALID_EMAIL_STATUS",
            f"Cannot fail non-sending emails. Current status is {email.status}",
        )

    # Update the email status to FAILED
    email.status = Email.Status.FAILED
    email.save()
    return email


@transaction.atomic
def email_send(to: str, subject: str) -> None:
    # Simulate potential email sending failure
    if settings.EMAIL_SENDING_FAILURE_TRIGGER:
        failure_dice = random.uniform(0, 1)
        if failure_dice <= settings.EMAIL_SENDING_FAILURE_RATE:
            raise ApplicationError("EMAIL_SEND_FAILURE", "Email sending failure triggered.")

    from_email = settings.EMAIL_HOST_USER
    plain_text = f"Your OTP is: {subject}"
    # Prepare the content of the email
    html = f"<p>Your OTP is: {plain_text}</p>"  # Assuming the subject contains the OTP

    try:
        # Prepare and send the email
        msg = EmailMultiAlternatives(subject, plain_text, from_email, [to])
        msg.attach_alternative(html, "text/html")
        msg.send()
    except Exception as e:
        # Log and raise an ApplicationError if sending fails
        raise ApplicationError("EMAIL_SEND_ERROR", f"Failed to send email: {str(e)}")


def email_send_all(emails: QuerySet[Email]):
    from .tasks import email_send as email_send_task

    for email in emails:
        with transaction.atomic():
            Email.objects.filter(id=email.id).update(status=Email.Status.SENDING)

        # Create a closure to capture the proper value of each id
        transaction.on_commit((lambda email_id: lambda: email_send_task.delay(email_id))(email.id))
