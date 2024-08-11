import io

from celery import shared_task
from celery.utils.log import get_task_logger
from django.conf import settings
from django.core.files.storage import default_storage
from django.template.loader import render_to_string
from django_weasyprint.utils import django_url_fetcher
from rest_framework.exceptions import ValidationError
from weasyprint import HTML

from config.env import BASE_URL
from core.common.utils import get_object
from core.participants.models import BaseParticipant

from .models import Incoming, Internal, Letter, Outgoing

logger = get_task_logger(__name__)


@shared_task(bind=True)
def generate_pdf_task(self, letter_id: str) -> Letter:
    letter_instance = get_object(Letter, id=letter_id)

    try:
        logger.info(f"Starting PDF generation for reference number: {letter_instance.reference_number}")

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

        pdf_io = io.BytesIO()
        weasy_html = HTML(
            string=html_content,
            url_fetcher=django_url_fetcher,
            base_url=settings.STATIC_URL,
        )

        weasy_html.write_pdf(pdf_io)
        pdf_io.seek(0)

        department = letter_instance.owner.department.name_en
        letter_ref_no = letter_instance.reference_number

        letter_pdf_path = f"letters/{department}/letter_{letter_ref_no}/letter_{letter_ref_no}.pdf"

        if default_storage.exists(letter_pdf_path):
            default_storage.delete(letter_pdf_path)

        default_storage.save(letter_pdf_path, pdf_io)

        letter_instance.pdf_version = default_storage.url(letter_pdf_path)
        letter_instance.save(update_fields=["pdf_version"])

        logger.info(f"PDF generation completed successfully for reference number: {letter_instance.reference_number}")
        return None

    except ValueError as e:
        logger.error(f"Error generating PDF for reference number: {letter_id}, error: {e}")
        raise ValidationError(e)

    except Exception as e:
        logger.error(f"Error generating PDF for reference number: {letter_id}, error: {e}")
        raise e
