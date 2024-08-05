import io
from collections import OrderedDict
from typing import Optional, Union

from django.conf import settings
from django.core.files.storage import default_storage
from django.db import transaction
from django.template.loader import render_to_string
from django_weasyprint.utils import django_url_fetcher
from weasyprint import HTML

from config.env import BASE_URL
from core.participants.models import Participant
from core.participants.services import participants_create
from core.participants.utils import identify_participants_changes
from core.users.models import Member
from core.workflows.services import letter_publish

from .models import Incoming, Internal, Letter, Outgoing

type LetterParticipant = dict[str, Union[str, int, dict[str, str], list[str]]]


# Create a letter instance based on the provided letter_type and keyword arguments.
def create_letter_instance(letter_type: str, **kwargs) -> Letter:
    letter_instance_class = {
        "internal": Internal,
        "incoming": Incoming,
        "outgoing": Outgoing,
    }.get(letter_type)

    if letter_instance_class:
        return letter_instance_class.objects.create(**kwargs)

    raise ValueError("Invalid letter type")


# This function orchestrates the creation of a letter and its participants
@transaction.atomic
def letter_create(
    *,
    current_user: Member,
    subject: Optional[str] = None,
    content: Optional[str] = None,
    letter_type: str,
    language: str,
    participants,
) -> Letter:
    letter_data = {
        "letter_type": letter_type,
        "subject": subject,
        "content": content,
        "current_state": Letter.States.DRAFT,
        "owner": current_user,
        "language": language,
    }

    letter_instance = create_letter_instance(**letter_data)

    if letter_type in ["internal", "outgoing"]:
        author_participant = OrderedDict({
            "id": "",
            "user": OrderedDict({
                "id": current_user.id,
                "user_type": "member",
            }),
            "role": "Author",
        })
        participants.append(author_participant)

    participants_create(
        current_user=current_user,
        letter_instance=letter_instance,
        participants=participants,
    )

    letter_generate_pdf(letter_instance=letter_instance)
    return letter_instance


@transaction.atomic
def letter_create_and_publish(
    *,
    current_user: Member,
    subject: Optional[str] = None,
    content: Optional[str] = None,
    signature=None,
    letter_type: str,
    participants,
) -> Letter:
    letter_data = {
        "letter_type": letter_type,
        "current_user": current_user,
        "subject": subject,
        "content": content,
        "current_state": Letter.States.DRAFT,
        "owner": current_user,
    }

    if signature is not None:
        letter_data["signature"] = signature

    letter_instance = create_letter_instance(**letter_data)

    letter_instance.current_state = Letter.States.SUBMITTED
    letter_instance.save()

    participants_create(
        current_user=current_user,
        letter_instance=letter_instance,
        participants=participants,
    )

    letter_publish(current_user=current_user, letter_instance=letter_instance)

    letter_generate_pdf(letter_instance=letter_instance)
    return letter_instance


@transaction.atomic
def letter_update(
    current_user: Member,
    letter_instance: Letter,
    subject: Optional[str] = None,
    content: Optional[str] = None,
    letter_type: str = "internal",
    participants: Optional[list[LetterParticipant]] = None,
) -> Letter:
    if subject is not None:
        letter_instance.subject = subject

    if content is not None:
        letter_instance.content = content

    letter_instance.save()

    participants_to_add, participants_to_remove = identify_participants_changes(
        letter_instance=letter_instance,
        new_participants=participants,
    )

    participants_to_remove.delete()

    participants_create(
        current_user=current_user,
        participants=participants_to_add,
        letter_instance=letter_instance,
    )

    letter_generate_pdf(letter_instance=letter_instance)
    return letter_instance


@transaction.atomic
def letter_move_to_trash(*, letter_instance=Letter):
    letter_instance.current_state = Letter.States.TRASHED
    letter_instance.save()

    return letter_instance


@transaction.atomic
def letter_restore_from_trash(*, letter_instance=Letter):
    letter_instance.current_state = Letter.States.DRAFT
    letter_instance.save()

    return letter_instance


@transaction.atomic
def letter_hide(*, letter_instance=Letter):
    letter_instance.hidden = True
    letter_instance.save()

    return letter_instance


@transaction.atomic
def letter_generate_pdf(letter_instance: Letter) -> Letter:
    primary_recipients = letter_instance.participants.filter(role=Participant.Roles.PRIMARY_RECIPIENT)
    cc_participants = letter_instance.participants.filter(role=Participant.Roles.CC)
    bcc_participants = letter_instance.participants.filter(role=Participant.Roles.BCC)

    context = {
        "letter": letter_instance,
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

    return letter_instance
