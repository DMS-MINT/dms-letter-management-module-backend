from django.db import transaction

from core.letters.models import Letter
from core.users.models import Member

from .models import Comment


@transaction.atomic
def comment_create(*, current_user=Member, letter_instance: Letter, content: str):
    Comment.objects.create(content=content, author=current_user, letter=letter_instance)


@transaction.atomic
def comment_update(*, comment_instance: Comment, content: str):
    comment_instance.content = content
    comment_instance.save()
