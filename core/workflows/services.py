from django.db import transaction
from django.utils import timezone
from rest_framework.exceptions import PermissionDenied

from core.letters.models import Incoming, Letter
from core.participants.models import Participant
from core.signatures.services import sign_letter
from core.users.models import User


@transaction.atomic
def letter_submit(*, current_user: User, letter_instance: Letter, signature_method: str) -> Letter:
    letter_instance.current_state = Letter.States.SUBMITTED
    letter_instance.submitted_at = timezone.now()

    letter_instance = sign_letter(
        letter_instance=letter_instance,
        current_user=current_user,
        signature_method=signature_method,
    )

    letter_instance.clean()
    letter_instance.save()

    participant = Participant.objects.get(letter=letter_instance, user=current_user)
    participant.clean()

    return letter_instance


@transaction.atomic
def letter_retract(current_user: User, letter_instance: Letter) -> Letter:
    participant = letter_instance.participants.get(user=current_user)
    administrator_participant = letter_instance.participants.filter(role=Participant.Roles.ADMINISTRATOR).first()

    if participant.role == Participant.Roles.AUTHOR:
        next_state = Letter.States.DRAFT
        letter_instance.submitted_at = None
        letter_instance.e_signatures.filter(signer=current_user).delete()

        if administrator_participant is not None:
            administrator_participant.delete()

    elif participant.role == Participant.Roles.ADMINISTRATOR:
        if isinstance(letter_instance, Incoming):
            next_state = Letter.States.DRAFT
        else:
            next_state = Letter.States.SUBMITTED

        administrator_participant.delete()

    else:
        raise PermissionDenied("You do not have permission to perform this action on this letter.")

    letter_instance.published_at = None
    letter_instance.current_state = next_state
    letter_instance.save()

    return letter_instance


@transaction.atomic
def letter_publish(current_user: User, letter_instance: Letter) -> Letter:
    current_state = Letter.States.SUBMITTED.value
    next_state = Letter.States.PUBLISHED.value

    if not isinstance(letter_instance, Incoming):
        if letter_instance.current_state != current_state:
            raise PermissionDenied("You can not perform this action on this letter in its current state.")

    for participant in letter_instance.participants.all():
        if participant.user == current_user:
            raise PermissionDenied("You cannot perform publishing actions on letters you are participating in.")

    letter_instance.clean()
    letter_instance.current_state = next_state
    letter_instance.published_at = timezone.now()
    letter_instance.save()

    participant_instance = Participant.objects.create(
        user=current_user,
        letter=letter_instance,
        role=Participant.Roles.ADMINISTRATOR,
        added_by=current_user,
    )

    participant_instance.clean()

    return letter_instance


@transaction.atomic
def letter_reject(current_user: User, letter_instance: Letter) -> Letter:
    letter_instance.published_at = None
    letter_instance.current_state = Letter.States.REJECTED
    letter_instance.save()

    return letter_instance


@transaction.atomic
def letter_close(*, current_user: User, letter_instance: Letter) -> Letter:
    letter_instance.clean()
    letter_instance.current_state = Letter.States.CLOSED
    letter_instance.save()

    participant = Participant.objects.get(letter=letter_instance, user=current_user)
    participant.clean()

    return letter_instance


@transaction.atomic
def letter_reopen(*, current_user: User, letter_instance: Letter) -> Letter:
    letter_instance.clean()
    letter_instance.current_state = Letter.States.PUBLISHED
    letter_instance.save()

    participant = Participant.objects.get(letter=letter_instance, user=current_user)
    participant.clean()

    return letter_instance
