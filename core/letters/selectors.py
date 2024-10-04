from django.conf import settings
from django.template.loader import render_to_string
from django_weasyprint.utils import django_url_fetcher
from weasyprint import HTML

from config.env import BASE_URL
from core.participants.models import BaseParticipant
from core.users.models.user import User

from .filters import BaseLetterFilter
from .models import Incoming, Internal, Letter, Outgoing


def letter_list(*, current_user=User, filters=None):
    filters = filters or {}

    qs = Letter.objects.filter(hidden=False)

    return BaseLetterFilter(filters, qs, current_user=current_user).qs


def letter_pdf(letter_instance):
    authors = letter_instance.participants.filter(role=BaseParticipant.Roles.AUTHOR)
    primary_recipients = letter_instance.participants.filter(role=BaseParticipant.Roles.PRIMARY_RECIPIENT)
    cc_participants = letter_instance.participants.filter(role=BaseParticipant.Roles.CC)
    bcc_participants = letter_instance.participants.filter(role=BaseParticipant.Roles.BCC)

    context = {
        "letter": letter_instance,
        "authors": authors,
        "primary_recipients": primary_recipients,
        "cc_participants": cc_participants,
        "bcc_participants": bcc_participants,
        "e_signatures": letter_instance.e_signatures.all(),
        "base_url": BASE_URL,
    }

    if isinstance(letter_instance, Internal):
        template_name = "internal_letter_template.html"
    elif isinstance(letter_instance, Outgoing):
        template_name = "outgoing_letter_template.html"
    elif isinstance(letter_instance, Incoming):
        template_name = "incoming_letter_template.html"
    else:
        raise ValueError("Unknown letter type")

    html_content = render_to_string(template_name=template_name, context=context)

    weasy_html = HTML(
        string=html_content,
        url_fetcher=django_url_fetcher,
        base_url=settings.STATIC_URL,
    )

    return weasy_html.write_pdf()
