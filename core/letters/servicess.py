from collections import OrderedDict
from typing import Optional, Union

from django.db import transaction

from core.participants.services import participants_create
from core.participants.utils import identify_participants_changes
from core.users.models import User
from core.workflows.services import letter_publish

from .models import Incoming, Internal, Letter, Outgoing

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
    participants,
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
            "user": OrderedDict({
                "id": current_user.id,
                "user_type": "User",
            }),
            "role": "Author",
        })
        participants.append(author_participant)

    participants_create(
        current_user=current_user,
        letter_instance=letter_instance,
        participants=participants,
    )

    return letter_instance


@transaction.atomic
def letter_create_and_publish(
    *,
    current_user: User,
    subject: Optional[str] = None,
    body: Optional[str] = None,
    letter_category: str,
    language: str,
    participants,
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

    return letter_instance


@transaction.atomic
def letter_update(
    current_user: User,
    letter_instance: Letter,
    subject: Optional[str] = None,
    body: Optional[str] = None,
    letter_category: str = "internal",
    participants: Optional[list[LetterParticipant]] = None,
) -> Letter:
    if subject is not None:
        letter_instance.subject = subject

    if body is not None:
        letter_instance.body = body

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
