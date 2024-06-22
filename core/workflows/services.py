from django.db import transaction
from rest_framework.exceptions import PermissionDenied

from core.letters.models import Letter
from core.participants.models import Participant
from core.participants.services import add_participants, remove_participants
from core.users.models import Member


@transaction.atomic
def letter_submit(*, current_user: Member, letter_instance: Letter) -> Letter:
    letter_instance.clean()
    letter_instance.current_state = Letter.States.SUBMITTED
    letter_instance.save()
    return letter_instance


@transaction.atomic
def letter_retract(current_user: Member, letter_instance: Letter) -> Letter:
    current_state = letter_instance.current_state
    next_state = Letter.States.SUBMITTED if current_state == Letter.States.PUBLISHED else Letter.States.DRAFT

    administrator_participant = {
        "to": [current_user.id],
        "role": Participant.Roles.ADMINISTRATOR.label,
    }

    remove_participants(
        current_user=current_user,
        letter_instance=letter_instance,
        participants=[administrator_participant],
    )

    letter_instance.current_state = next_state
    letter_instance.save()
    return letter_instance


@transaction.atomic
def letter_publish(current_user: Member, letter_instance: Letter) -> Letter:
    current_state = Letter.States.SUBMITTED.value
    next_state = Letter.States.PUBLISHED.value

    if letter_instance.current_state != current_state:
        raise PermissionDenied("You can not perform this action on this letter in its current state.")

    for participant in letter_instance.participants.all():
        if participant.user == current_user:
            raise PermissionDenied("You cannot perform publishing actions on letters you are participating in.")

    letter_instance.clean()
    letter_instance.current_state = next_state
    letter_instance.save()

    administrator_participant = {
        "to": [current_user.id],
        "role": Participant.Roles.ADMINISTRATOR.label,
    }

    add_participants(
        current_user=current_user,
        letter_instance=letter_instance,
        participants=[administrator_participant],
    )

    return letter_instance
