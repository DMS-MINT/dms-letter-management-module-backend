from django.core.exceptions import ObjectDoesNotExist, ValidationError
from django.db import transaction
from django.utils.translation import gettext_lazy as _

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
def initialize_participants(*, current_user: Member, participants, letter_instance):
    current_user_exists = next(
        (participant for participant in participants if participant["user"]["id"] == current_user.id),
        None,
    )
    if current_user_exists:
        # CREATOR MUST BE AN EDITOR OR AUTHOR NO OTHER ROLES ARE ALLOWED
        pass
    else:
        Participant.objects.create(
            user=current_user,
            letter=letter_instance,
            role_name=Participant.RoleNames.EDITOR,
        )
    if participants:
        for participant in participants:
            role_name = get_enum_value(participant["role_name"])
            user_data = participant["user"]

            if user_data["user_type"] == "member":
                try:
                    user = Member.objects.get(pk=user_data["id"])
                    if user == current_user and role_name not in [
                        Participant.RoleNames.AUTHOR,
                        Participant.RoleNames.EDITOR,
                    ]:
                        raise ValidationError(
                            _(  # noqa: F823
                                f"You cannot be assigned the role of '{participant.get_role_name_display()}' because you are composing the letter.",  # noqa: E501
                            ),
                        )
                except Member.DoesNotExist as e:
                    raise ObjectDoesNotExist(f"Member with ID {user_data["id"]} does not exist. Error: {e}")

            elif user_data["user_type"] == "guest":
                user, _ = Guest.objects.get_or_create(name=user_data["name"])

            Participant.objects.create(user=user, role_name=role_name, letter=letter_instance)

    return


def update_participants(*, current_user: Member, letter_instance, participants_to_add):
    if participants_to_add:
        for participant in participants_to_add:
            role_name = get_enum_value(participant["role_name"])
            user_data = participant["user"]

            if user_data["user_type"] == "member":
                user = Member.objects.get(pk=user_data["id"])
                if user == current_user:
                    if role_name == Participant.RoleNames.AUTHOR:
                        Participant.objects.get(letter=letter_instance, user=user).delete()
                        Participant.objects.create(
                            letter=letter_instance,
                            user=user,
                            role_name=Participant.RoleNames.AUTHOR,
                        )
                        return

                    raise ValidationError("You cannot send a letter to yourself as a recipient.")

            elif user_data["user_type"] == "guest":
                user, _ = Guest.objects.get_or_create(name=user_data["name"])

            Participant.objects.create(user=user, role_name=role_name, letter=letter_instance)

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
        participant_instance = Participant.objects.create(
            user=user,
            role_name=role_name,
            letter=letter_instance,
        )
        participant_instance.permissions.set(permission_objects)

    return participant_instance
