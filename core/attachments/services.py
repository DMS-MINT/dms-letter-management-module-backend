from django.db import transaction

from core.letters.models import Letter
from core.users.models import User

from .models import Attachment


@transaction.atomic
def attachment_create(
    current_user: User,
    letter_instance: Letter,
    attachments,
):
    for attachment in attachments:
        Attachment.objects.create(
            letter=letter_instance,
            file=attachment,
            uploaded_by=current_user,
        )
