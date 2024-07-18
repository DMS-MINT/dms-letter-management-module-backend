from django.core.mail import EmailMultiAlternatives
from django.db import transaction
from django.db.models.query import QuerySet
from django.utils import timezone

from core.api.exceptions import ApplicationError

from .models import Email
from .tasks import email_send as email_send_task


@transaction.atomic
def email_failed(email_instance: Email):
    if email_instance.status != Email.Status.SENDING:
        raise ApplicationError(f"Cannot fail non-sending emails. Current status is {email_instance.status}")

    email_instance.status = Email.Status.FAILED
    return email_instance


@transaction.atomic
def email_send(email_instance: Email):
    if email_instance.status != Email.Status.SENDING:
        raise ApplicationError(f"Cannot send non-ready emails. Current status is {email_instance.status}")

    subject = email_instance.subject
    from_email = "yabilisanu@gmail.com"
    to = email_instance.to.email

    html = email_instance.html
    plain_text = email_instance.plain_text

    msg = EmailMultiAlternatives(subject, plain_text, from_email, [to])
    msg.attach_alternative(html, "text/html")

    msg.send()

    email_instance.status = Email.Status.SENT
    email_instance.sent_at = timezone.now()

    return email_instance


def email_send_all(emails: QuerySet(Email)):
    for email in emails:
        with transaction.atomic():
            Email.objects.filter(id=email.id).update(status=Email.Status.SENDING)

        transaction.on_commit((lambda email_id: lambda: email_send_task.delay(email_id))(email.id))
