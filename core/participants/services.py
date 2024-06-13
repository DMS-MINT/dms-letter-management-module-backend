from django.core.exceptions import ObjectDoesNotExist
from django.db import transaction

from core.users.models import Guest, Member

from .models import Participant, Role


# This function create participants for a given letter.
@transaction.atomic
def participant_create(*, participants, letter):
    letter_participants = []
    for participant in participants:
        user_data = participant.get("user")
        role_name = participant.get("role")
        role = Role.objects.get(name=role_name)

        if user_data["user_type"] == "member":
            try:
                user = Member.objects.get(id=user_data["id"])
            except Member.DoesNotExist as e:
                raise ObjectDoesNotExist(f"Member with ID {user_data["id"]} does not exist. Error: {e}")
        elif user_data["user_type"] == "guest":
            user, _ = Guest.objects.get_or_create(name=user_data["name"])

        participant_instance = Participant.objects.create(user=user, role=role, letter=letter)
        letter_participants.append(participant_instance)

    return letter_participants
