from collections import OrderedDict
from typing import Optional, Union

from django.db import transaction

from core.participants.services import participants_create
from core.users.models import User
from core.workflows.services import letter_publish

from ..models import Incoming, Internal, Letter, Outgoing
from ..tasks import generate_pdf_task

type LetterParticipant = dict[str, Union[str, int, dict[str, str], list[str]]]


# Create a letter instance based on the provided letter_category and keyword arguments.
def create_letter_instance(letter_category: str, **kwargs) -> Letter:
    letter_instance_class = {
        "internal": Internal,
        "incoming": Incoming,
        "outgoing": Outgoing,
    }.get(letter_category)

    if letter_instance_class:
        return letter_instance_class.objects.create(**kwargs)

    raise ValueError("Invalid letter type")


@transaction.atomic
def letter_create(
    *,
    current_user: User,
    subject: Optional[str] = None,
    body: Optional[str] = None,
    letter_category: str,
    language: str,
    participants: Optional[list[LetterParticipant]] = None,
) -> Letter:
    letter_data = {
        "letter_category": letter_category,
        "subject": subject,
        "body": body,
        "current_state": Letter.States.DRAFT,
        "owner": current_user,
        "language": language,
    }

    letter_instance = create_letter_instance(**letter_data)

    if letter_category in ["internal", "outgoing"]:
        author_participant = OrderedDict({
            "id": "",
            "user_id": current_user.id,
            "role": 1,
            "participant_type": "user",
        })
        participants.append(author_participant)

    participants_create(current_user=current_user, letter_instance=letter_instance, participants=participants)

    generate_pdf_task.delay_on_commit(letter_id=letter_instance.id)

    return letter_instance


@transaction.atomic
def letter_create_and_publish(
    *,
    current_user: User,
    subject: Optional[str] = None,
    body: Optional[str] = None,
    letter_category: str,
    language: str,
    participants: Optional[list[LetterParticipant]] = None,
) -> Letter:
    letter_data = {
        "letter_category": letter_category,
        "subject": subject,
        "body": body,
        "current_state": Letter.States.DRAFT,
        "owner": current_user,
        "language": language,
    }

    letter_instance = create_letter_instance(**letter_data)

    letter_instance.current_state = Letter.States.SUBMITTED
    letter_instance.save()

    participants_create(
        current_user=current_user,
        letter_instance=letter_instance,
        participants=participants,
    )

    letter_publish(current_user=current_user, letter_instance=letter_instance)

    generate_pdf_task.delay_on_commit(letter_id=letter_instance.id)

    return letter_instance
