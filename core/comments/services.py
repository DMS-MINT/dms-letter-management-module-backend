from django.db import transaction

from core.letters.models import Letter
from core.users.models import User

from .models import Comment


@transaction.atomic
def comment_create(*, current_user=User, letter_instance: Letter, message: str):
    Comment.objects.create(message=message, author=current_user, letter=letter_instance)


@transaction.atomic
def comment_update(*, comment_instance: Comment, message: str):
    comment_instance.message = message
    comment_instance.save()
