from core.letters.models import Letter
from core.notifications.models import Tag
from core.notifications.services import notification_create, notification_send
from core.participants.models import BaseParticipant
from core.users.models import User

# def handle_mention_notification(
#     *,
#     current_user: User,
#     message: str,
#     letter_instance: Letter,
#     participants: BaseParticipant,
# ):
#     letter_tag, _ = Tag.objects.get_or_create(name="Letter")
#     mention_tag, _ = Tag.objects.get_or_create(name="Mention")
#     collaboration_tag, _ = Tag.objects.get_or_create(name="Collaboration")

#     tags = [letter_tag, mention_tag, collaboration_tag]
#     subject = f"አዲስ የትብብር ጥያቄ፡ ደብዳቤ {letter_instance.reference_number}"


#     # recipient_ids = collaborator_participants.values_list("internaluserparticipant__user__id", flat=True)

#     notification_instance = notification_create(
#         to=list(recipient_ids),
#         subject=subject,
#         message=message,
#         tags=tags,
#         channels=[],
#         details={
#             "source": "user",
#             "letter_ref": letter_instance.reference_number,
#             "sender": {
#                 "full_name": current_user.full_name_am,
#                 "job_title": current_user.job_title.title_am,
#             },
#         },
#     )

#     notification_send(notification_instance=notification_instance)


def handle_publish_letter_notification(*, current_user: User, letter_instance: Letter):
    letter_tag, _ = Tag.objects.get_or_create(name="Letter")
    workflow_tag, _ = Tag.objects.get_or_create(name="Workflow")
    published_tag, _ = Tag.objects.get_or_create(name="Published")

    tags = [letter_tag, workflow_tag, published_tag]
    subject = f"Letter {letter_instance.reference_number} has been published by the record office"
    message = f"Your letter with reference number {letter_instance.reference_number} has been published by the record office and distributed to all recipients. The letter cannot be edited at this stage, but you can retract it if changes are needed."  # noqa: E501

    author_participants = letter_instance.participants.filter(
        role=BaseParticipant.Roles.AUTHOR,
        polymorphic_ctype__model="internaluserparticipant",
    ).select_related("internaluserparticipant__user")

    recipient_ids = author_participants.values_list("internaluserparticipant__user__id", flat=True)

    notification_instance = notification_create(
        to=list(recipient_ids),
        subject=subject,
        message=message,
        tags=tags,
        channels=[],
        details={
            "source": "user",
            "letter_ref": letter_instance.reference_number,
            "sender": {
                "full_name": current_user.full_name_am,
                "job_title": current_user.job_title.title_am,
            },
        },
    )

    notification_send(notification_instance=notification_instance)


def handle_reject_letter_notification(*, current_user: User, letter_instance: Letter, message: str):
    letter_tag, _ = Tag.objects.get_or_create(name="Letter")
    workflow_tag, _ = Tag.objects.get_or_create(name="Workflow")
    rejected_tag, _ = Tag.objects.get_or_create(name="Rejected")

    tags = [letter_tag, workflow_tag, rejected_tag]
    subject = f"Letter {letter_instance.reference_number} has been rejected by the record office"

    author_participants = letter_instance.participants.filter(
        role=BaseParticipant.Roles.AUTHOR,
        polymorphic_ctype__model="internaluserparticipant",
    ).select_related("internaluserparticipant__user")

    recipient_ids = author_participants.values_list("internaluserparticipant__user__id", flat=True)

    notification_instance = notification_create(
        to=list(recipient_ids),
        subject=subject,
        message=message,
        tags=tags,
        channels=[],
        details={
            "source": "user",
            "letter_ref": letter_instance.reference_number,
            "sender": {
                "full_name": current_user.full_name_am,
                "job_title": current_user.job_title.title_am,
            },
        },
    )

    notification_send(notification_instance=notification_instance)
