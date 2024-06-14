from django.core.exceptions import ObjectDoesNotExist
from rest_framework.exceptions import PermissionDenied

from .models import Permission


def check_permissions(letter_instance, user, actions: list):
    for action in actions:
        action = action.lower()
        if not Permission.objects.filter(name=action).exists():
            raise ObjectDoesNotExist(f"{action} does not exist.")

        letter_participants = letter_instance.participants.filter(user=user)

        if not letter_participants.exists():
            raise PermissionDenied("You are not a participant in this letter.")

        if not letter_instance.state.can(action):
            raise PermissionDenied(f"The letter cannot be {action} in its current state.")

        if not any(participant.can(action) for participant in letter_participants):
            raise PermissionDenied(f"You do not have permission to {action} this letter.")

    return True
