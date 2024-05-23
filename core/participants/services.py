from django.core.exceptions import ObjectDoesNotExist
from django.db import transaction

from core.letters.models import Letter
from core.users.models import BaseUser
from core.users.services import guest_create

from .models import Participant


@transaction.atomic
def participant_create(*, validated_data, letter_id):
    try:
        letter = Letter.objects.get(id=letter_id)
    except ObjectDoesNotExist:
        raise ValueError(f"Letter with id {letter_id} does not exist")

    participants = []
    for data in validated_data:
        user_data = data["user"]
        role = data["role"]
        message = data.get("message", "")

        try:
            if user_data["user_type"] == "member":
                user_id = user_data["id"]
                user = BaseUser.objects.get(id=user_id)
            elif user_data["user_type"] == "guest":
                user = guest_create(validated_data=user_data)
            else:
                raise ValueError(f"Invalid user_type: {user_data['user_type']}")

            participant = Participant.objects.create(user=user, role=role, letter=letter, message=message)
            participants.append(participant)
        except Exception as e:
            raise ValueError(f"Unable to create participant: {e}")

    return participants
