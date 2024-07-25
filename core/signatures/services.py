from django.db import transaction
from rest_framework import status as http_status

from core.api.exceptions import APIError
from core.letters.models import Letter
from core.users.models import Member

from .models import Signature


@transaction.atomic
def sign_letter(*, letter_instance: Letter, current_user: Member):
    try:
        e_signature_instance = Signature.objects.get(user=current_user)

    except Signature.DoesNotExist:
        raise APIError(
            error_code="SIGNATURE_NOT_FOUND",
            status_code=http_status.HTTP_404_NOT_FOUND,
            message="Not Found Error",
            extra={"e_signature": "The signature for the specified user does not exist."},
        )

    letter_instance.e_signature.add(e_signature_instance)
    letter_instance.save()

    return letter_instance
