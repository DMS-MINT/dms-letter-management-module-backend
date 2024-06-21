from django.db import transaction

from core.letters.models import Letter

# from core.participants.services import participant_add
from core.users.models import Member


@transaction.atomic
def letter_submit(*, current_user: Member, letter_instance: Letter) -> Letter:
    letter_instance.clean()
    letter_instance.current_state = Letter.States.SUBMITTED
    letter_instance.save()
    return letter_instance


@transaction.atomic
def letter_retract(user: Member, letter_instance: Letter) -> Letter:
    current_state = letter_instance.current_state
    next_state = "Submitted" if f"{current_state}" == "Published" else "Draft"

    letter_instance.current_state = Letter.States[next_state.capitalize()]
    letter_instance.save()
    return letter_instance


@transaction.atomic
def letter_publish(user: Member, letter_instance: Letter) -> Letter:
    current_state = Letter.States.SUBMITTED
    next_state = Letter.States.PUBLISHED

    if letter_instance.current_state != current_state or not user.is_admin:
        raise PermissionError("User does not have permission to publish letter.")

    letter_instance.state = next_state
    letter_instance.save()

    return letter_instance
