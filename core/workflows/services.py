from django.db import transaction

from core.letters.models import Letter, State
from core.participants.services import participant_add
from core.permissions.service import check_permission
from core.users.models import Member


@transaction.atomic
def letter_share(
    user: Member,
    letter_instance: Letter,
    to: str,
    message: str,
    permissions: list[str] = ["view"],
) -> Letter:
    check_permission(letter_instance, user, "share")

    collaborator = Member.objects.get(pk=to)
    participant_add(user=collaborator, letter_instance=letter_instance, permissions=permissions)


@transaction.atomic
def letter_submit(user: Member, letter_instance: Letter) -> Letter:
    check_permission(letter_instance, user, "submit")

    letter_instance.state = State.objects.get(name="Submitted")
    letter_instance.save()


@transaction.atomic
def letter_retract(user: Member, letter_instance: Letter) -> Letter:
    check_permission(letter_instance, user, "retract")

    letter_instance.state = State.objects.get(name="Draft")
    letter_instance.save()


@transaction.atomic
def letter_publish(user: Member, letter_instance: Letter) -> Letter:
    submitted_state = State.objects.get(name="Submitted")
    published_state = State.objects.get(name="Published")

    if letter_instance.state != submitted_state or not user.is_admin:
        raise PermissionError("User does not have permission to publish letter.")

    letter_instance.state = published_state
    letter_instance.save()
