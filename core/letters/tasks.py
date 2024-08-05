import io

from celery.utils.log import get_task_logger
from django.core.files.storage import default_storage
from django.template.loader import render_to_string
from weasyprint import HTML

from config import shared_task
from core.common.utils import get_object

logger = get_task_logger(__name__)


@shared_task(bind=True, max_retries=3)
def letter_generate_pdf_task(self, letter_id: str):
    from core.letters.models import Letter

    letter_instance = get_object(Letter, id=letter_id)

    try:
        template_name = "report.html"
        context = {
            "title": "My Report Title",
            "body": "This is the body of the report.",
        }

        html_string = render_to_string(template_name=template_name, context=context)

        pdf_io = io.BytesIO()
        HTML(string=html_string).write_pdf(pdf_io)
        pdf_io.seek(0)

        department = letter_instance.owner.department.name_en
        letter_ref_no = letter_instance.reference_number

        letter_pdf_path = f"letters/{department}/letter-{letter_ref_no}/letter-{letter_ref_no}.pdf"
        default_storage.save(letter_pdf_path, pdf_io)

        letter_instance.pdf_version = default_storage.url(letter_pdf_path)
        letter_instance.save(update_fields=["pdf_version"])

    except Exception as e:
        # https://docs.celeryq.dev/en/stable/userguide/tasks.html#retrying
        logger.error(f"An error occurred while generating the PDF for letter id {letter_id}: {e}")
        self.retry(exc=e, countdown=5)
