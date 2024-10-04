from django.db import transaction

from core.common.utils import get_object
from core.letters.models import Letter
from core.signatures.models import LetterSignature, Signature, UserDefaultSignature
from core.users.models.user import User


def get_enum_value(key: str) -> int:
    for method in Signature.Methods:
        if method.label.lower() == key.lower():
            return method.value
    raise ValueError(f"No matching signing method value for key: {key}")


@transaction.atomic
def sign_letter(*, letter_instance: Letter, current_user: User, signature_method: str):
    user_default_signature = get_object(UserDefaultSignature, user=current_user)
    signature_method_value = get_enum_value(signature_method)

    LetterSignature.objects.create(
        signer=current_user,
        signature_method=signature_method_value,
        signature_image=user_default_signature.signature_image,
        letter=letter_instance,
    )

    return letter_instance
