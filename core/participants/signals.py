# from django.core.exceptions import ValidationError
from django.db.models.signals import post_save

# from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver

# from django.utils.translation import gettext_lazy as _
from .models import Participant
from .utils import get_permissions

# @receiver(pre_save, sender=Participant)
# def validate_participant_role(sender, instance, **kwargs):
#     current_user = instance._current_user
#     if instance.user == current_user and instance.role_name not in [
#         Participant.RoleNames.AUTHOR,
#         Participant.RoleNames.EDITOR,
#     ]:
#         raise ValidationError(
#             _(
#                 f"You cannot be assigned the role of '{instance.get_role_name_display()}' because you are composing the letter.",  # noqa: E501
#             ),
#         )


@receiver(post_save, sender=Participant)
def assign_default_permissions(sender, instance, created, **kwargs):
    # current_user = instance._current_user
    # letter_instance = instance.letter

    # if not Participant.objects.filter(user=current_user, letter=letter_instance).exists():
    #     participant_instance = Participant(
    #         user=current_user,
    #         letter=letter_instance,
    #         role_name=Participant.RoleNames.EDITOR,
    #     )
    #     participant_instance.save()

    if created and instance._dirty:
        permissions = get_permissions(instance.role_name)
        instance.permissions.set(permissions)
        instance._dirty = False
        instance.save()
