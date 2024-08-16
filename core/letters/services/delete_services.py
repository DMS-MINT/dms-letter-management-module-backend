from django.db import transaction

from core.letters.models import Letter


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
