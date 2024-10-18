import random

from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from django.db import transaction
from django.template.loader import render_to_string
from django.utils import timezone

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
    html = f"<p>Your OTP is: {plain_text}</p>"

    try:
        # Prepare and send the email
        msg = EmailMultiAlternatives(subject, plain_text, from_email, [to])
        msg.attach_alternative(html, "text/html")
        msg.send()
    except Exception as e:
        # Log and raise an ApplicationError if sending fails
        raise ApplicationError("EMAIL_SEND_ERROR", f"Failed to send email: {str(e)}")


# def email_send_all(emails: QuerySet[Email]):

#     from .tasks import email_send as email_send_task

#     for email in emails:
#         with transaction.atomic():
#             Email.objects.filter(id=email.id).update(status=Email.Status.SENDING)

#         # Create a closure to capture the proper value of each id
#         transaction.on_commit((lambda email_id: lambda: email_send_task.delay(email_id))(email.id))


def email_send_type(to: str, subject: str, template_name: str, context: dict) -> str:
    # Simulate potential email sending failure
    if settings.EMAIL_SENDING_FAILURE_TRIGGER:
        failure_dice = random.uniform(0, 1)
        if failure_dice <= settings.EMAIL_SENDING_FAILURE_RATE:
            raise ApplicationError("EMAIL_SEND_FAILURE", "Email sending failure triggered.")

    from_email = settings.EMAIL_HOST_USER

    html = render_to_string(f"email_templates/{template_name}/email.html", context)
    plain_text = render_to_string(f"email_templates/{template_name}/email_text.txt", context)

    try:
        msg = EmailMultiAlternatives(subject, plain_text, from_email, [to])
        msg.attach_alternative(html, "text/html")
        msg.send()

        email_instance = Email(
            status=Email.Status.SENT,
            to=to,
            subject=subject,
            html=html,
            plain_text=plain_text,
            sent_at=timezone.now(),
        )
        email_instance.save()

        return html

    except Exception as e:
        raise ApplicationError("EMAIL_SEND_ERROR", f"Failed to send email: {str(e)}")
