import io

from django.template.loader import render_to_string
from weasyprint import HTML

from core.participants.models import Participant
from core.users.models import Member

from .filters import BaseLetterFilter
from .models import Incoming, Internal, Letter, Outgoing


def letter_list(*, current_user=Member, filters=None):
    filters = filters or {}

    qs = Letter.objects.filter(hidden=False)

    return BaseLetterFilter(filters, qs, current_user=current_user).qs


def letter_pdf(*, letter_instance: Letter):
    primary_recipients = letter_instance.participants.filter(role=Participant.Roles.PRIMARY_RECIPIENT)
    cc_participants = letter_instance.participants.filter(role=Participant.Roles.CC)
    bcc_participants = letter_instance.participants.filter(role=Participant.Roles.BCC)

    context = {
        "letter": letter_instance,
        "primary_recipients": primary_recipients,
        "cc_participants": cc_participants,
        "bcc_participants": bcc_participants,
    }

    if isinstance(letter_instance, Internal):
        template_name = "internal_letter_template.html"
    elif isinstance(letter_instance, Outgoing):
        template_name = "outgoing_letter_template.html"
    elif isinstance(letter_instance, Incoming):
        template_name = "incoming_letter_template.html"
    else:
        raise ValueError("Unknown letter type")

    html_string = render_to_string(template_name, context)

    return HTML(string=html_string).write_pdf()


def generate_pdf():
    template_name = "report.html"
    context = {
        "title": "My Report Title",
        "body": "This is the body of the report.",
    }

    html_string = render_to_string(template_name=template_name, context=context)

    pdf_io = io.BytesIO()
    HTML(string=html_string).write_pdf(pdf_io)
    pdf_io.seek(0)

    return pdf_io
