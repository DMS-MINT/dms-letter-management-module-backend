from django.core.exceptions import ObjectDoesNotExist
from django.db import transaction

from core.letters.models import Letter
from core.permissions.models import Permission
from core.users.models import Guest, Member

from .models import Participant


def get_enum_value(key: str):
    for role in Participant.RoleNames:
        if role.label.lower() == key.lower():
            return role.value
    raise ValueError(f"No matching participant role value for key: {key}")


# This function create participants for a given letter.
@transaction.atomic
def participant_create(*, current_user: Member, participants, letter_instance):
    if participants:
        for participant in participants:
            role_name = get_enum_value(participant["role_name"])
            user_data = participant["user"]
            # permissions = get_permissions(role_name)

            if user_data["user_type"] == "member":
                try:
                    user = Member.objects.get(pk=user_data["id"])
                except Member.DoesNotExist as e:
                    raise ObjectDoesNotExist(f"Member with ID {user_data["id"]} does not exist. Error: {e}")

            elif user_data["user_type"] == "guest":
                user, _ = Guest.objects.get_or_create(name=user_data["name"])

            participant_instance = Participant(user=user, role_name=role_name, letter=letter_instance)
            participant_instance.save(current_user=current_user)
            # participant_instance.permissions.set(permissions)

    return


# This function adds participants for a given letter.
@transaction.atomic
def participant_add(*, user: Member, letter_instance: Letter, permissions: list[str]):
    role_name = Participant.RoleNames.COLLABORATOR

    permission_objects = Permission.objects.filter(name__in=permissions)
    if permission_objects.count() != len(permissions):
        missing_permissions = set(permissions) - set(permission_objects.values_list("name", flat=True))
        raise ValueError(f"Invalid permission names: {missing_permissions}")

    participant_instance = letter_instance.participants.filter(user=user).first()

    if participant_instance is not None:
        current_permissions = set(participant_instance.permissions.values_list("name", flat=True))
        new_permissions = set(permission_objects.values_list("name", flat=True))

        combined_permissions = current_permissions.union(new_permissions)

        participant_instance.permissions.set(Permission.objects.filter(name__in=combined_permissions))
    else:
        participant_instance = Participant.objects.create(user=user, role_name=role_name, letter=letter_instance)
        participant_instance.permissions.set(permission_objects)

    return participant_instance

    # if participants:
    #     for participant in participants:
    #         user_data = participant.get("user")
    #         role_name = get_enum_value(participant.get("role_name"))
    #         if user_data["user_type"] == "member":
    #             try:
    #                 user = Member.objects.get(id=user_data["id"])
    #             except Member.DoesNotExist as e:
    #                 raise ObjectDoesNotExist(f"Member with ID {user_data["id"]} does not exist. Error: {e}")

    #         elif user_data["user_type"] == "guest":
    #             user, _ = Guest.objects.get_or_create(name=user_data["name"])

    #         Participant.objects.create(user=user, role_name=role_name, letter=letter_instance)
