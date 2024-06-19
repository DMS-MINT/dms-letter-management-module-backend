from django.db import transaction

from core.comments.services import comment_create
from core.letters.models import Letter, State

# from core.participants.services import participant_add
from core.users.models import Member


@transaction.atomic
def letter_share(
    user: Member,
    letter_instance: Letter,
    to: str,
    message: str,
    permissions: list[str] = ["view", "comment"],
) -> Letter:
    collaborator = Member.objects.get(pk=to)
    # participant_add(user=collaborator, letter_instance=letter_instance, permissions=permissions)
    comment_create(user=user, letter_instance=letter_instance, content=message)


@transaction.atomic
def letter_submit(user: Member, letter_instance: Letter) -> Letter:
    letter_instance.current_state = State.objects.get(name="Submitted")
    letter_instance.save()


@transaction.atomic
def letter_retract(user: Member, letter_instance: Letter) -> Letter:
    letter_instance.current_state = State.objects.get(name="Draft")
    letter_instance.save()


@transaction.atomic
def letter_publish(user: Member, letter_instance: Letter) -> Letter:
    current_state = State.objects.get(name="Submitted")
    next_state = State.objects.get(name="Published")

    if letter_instance.current_state != current_state or not user.is_admin:
        raise PermissionError("User does not have permission to publish letter.")

    letter_instance.state = next_state
    letter_instance.save()
