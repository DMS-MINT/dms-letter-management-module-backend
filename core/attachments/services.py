from django.core.files.uploadedfile import InMemoryUploadedFile
from django.db import transaction

from core.letters.models import Letter
from core.users.models.user import User

from .models import LetterAttachment


@transaction.atomic
def letter_attachment_create(
    current_user: User,
    letter_instance: Letter,
    attachments,
):
    for attachment in attachments:
        file = attachment.get("file")
        description = attachment.get("description", "")

        if isinstance(file, InMemoryUploadedFile):
            LetterAttachment.objects.create(
                file=file,
                file_name=file.name,
                file_type=file.content_type,
                file_size=file.size,
                description=description,
                letter=letter_instance,
                uploaded_by=current_user,
            )
