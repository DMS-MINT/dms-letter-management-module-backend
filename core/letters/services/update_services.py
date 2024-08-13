from typing import Optional, Union

from django.db import transaction

from core.letters.models import Letter
from core.letters.tasks import generate_pdf_task
from core.participants.services import participants_create
from core.participants.utils import identify_participants_changes
from core.users.models import User

type LetterParticipant = dict[str, Union[str, int, dict[str, str], list[str]]]


@transaction.atomic
def letter_update(
    *,
    current_user: User,
    letter_instance: Letter,
    subject: Optional[str] = None,
    body: Optional[str] = None,
    language: Optional[str],
    participants: Optional[list[LetterParticipant]] = None,
) -> Letter:
    if subject is not None:
        letter_instance.subject = subject

    if body is not None:
        letter_instance.body = body

    letter_instance.language = language

    letter_instance.save()

    participants_to_add, participants_to_remove = identify_participants_changes(
        letter_instance=letter_instance,
        new_participants=participants,
    )

    participants_to_remove.delete()

    participants_create(
        current_user=current_user,
        letter_instance=letter_instance,
        participants=participants_to_add,
    )

    generate_pdf_task.delay_on_commit(letter_id=letter_instance.id)

    return letter_instance
