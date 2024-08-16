import os

from django.conf import settings
from django.db import models
from django.utils.translation import gettext_lazy as _

from core.comments.models import BaseModel


def signature_directory_path(instance, filename):
    if hasattr(instance, "user"):
        # For UserDefaultSignature
        department = instance.user.department.name_en
        user_id = instance.user.id
        return f"users/{department}/user_{user_id}/default_signature.png"

    if hasattr(instance, "letter"):
        # For LetterSignature
        department = instance.signer.department.name_en
        letter_ref_no = instance.letter.reference_number
        user_id = instance.signer.id
        return f"letters/{department}/letter_{letter_ref_no}/signatures/user_{user_id}.png"

    if hasattr(instance, "document"):
        # For DocumentSignature
        department = instance.signer.department.name_en
        doc_ref_no = ""  # Set the document reference number here
        user_id = instance.signer.id
        return f"documents/{department}/documents_{doc_ref_no}/signatures/user_{user_id}.png"

    # Default fallback path
    return f"fallback/signatures/{filename}"


class Signature(BaseModel):
    class Methods(models.IntegerChoices):
        Default = 1, _("Default")
        Canvas = 2, _("Canvas")

    signer = models.ForeignKey(
        "users.User",
        on_delete=models.CASCADE,
        related_name="signed_%(class)s",
        verbose_name=_("Signer"),
    )
    signature_image = models.ImageField(upload_to=signature_directory_path, verbose_name=_("Signature Image"))
    signature_method = models.IntegerField(choices=Methods.choices, verbose_name=_("Signature Method"))

    @property
    def signature_url(self):
        if self.signature_image:
            return os.path.join(settings.MEDIA_URL, self.signature_image.name)
        return ""

    def __str__(self):
        return f"{self.signer.full_name}'s signature"

    class Meta:
        abstract = True


class LetterSignature(Signature):
    letter = models.ForeignKey(
        "letters.Letter",
        on_delete=models.CASCADE,
        related_name="e_signatures",
        verbose_name=_("Letter"),
    )

    class Meta(Signature.Meta):
        db_table = "letter_signature"
        verbose_name = _("Letter Signature")
        verbose_name_plural = _("Letter Signatures")


class UserDefaultSignature(BaseModel):
    user = models.ForeignKey(
        "users.User",
        on_delete=models.CASCADE,
        related_name="default_signature",
        verbose_name=_("User"),
    )
    signature_image = models.ImageField(upload_to=signature_directory_path, verbose_name=_("Signature Image"))

    @property
    def signature_url(self):
        if self.signature_image:
            return os.path.join(settings.MEDIA_URL, self.signature_image.name)
        return ""

    def __str__(self):
        return f"{self.user.full_name}'s signature"
