from django.core.exceptions import ObjectDoesNotExist
from rest_framework.exceptions import PermissionDenied

from .models import Permission


def check_permission(letter_instance, user, action: str):
    if not Permission.objects.filter(name=action.lower()).exists():
        raise ObjectDoesNotExist(f"{action} does not exist.")

    letter_participants = letter_instance.participants.filter(user=user)

    if not letter_participants.exists():
        raise PermissionDenied("You are not a participant in this letter.")

    if not letter_instance.state.can(action.lower()):
        raise PermissionDenied(f"The letter cannot be {action.lower()} in its current state.")

    if not any(participant.can(action.lower()) for participant in letter_participants):
        raise PermissionDenied(f"You do not have permission to {action.lower()} this letter.")

    return True
