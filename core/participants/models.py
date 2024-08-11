from django.core.exceptions import ValidationError
from django.db import models
from django.utils.translation import gettext_lazy as _
from polymorphic.models import PolymorphicModel

from core.common.models import BaseModel
from core.letters.models import Internal, Outgoing
from core.permissions.service import assign_permissions, remove_permissions


class BaseParticipant(PolymorphicModel, BaseModel):
    class Roles(models.IntegerChoices):
        AUTHOR = 1, _("Author")
        PRIMARY_RECIPIENT = 2, _("Primary Recipient")
        CC = 3, _("Carbon Copy Recipient")
        BCC = 4, _("Blind Carbon Copy Recipient")
        COLLABORATOR = 5, _("Collaborator")
        ADMINISTRATOR = 6, _("Administrator")

    role = models.IntegerField(choices=Roles.choices, verbose_name=_("Roles"))
    letter = models.ForeignKey("letters.Letter", on_delete=models.CASCADE, related_name="participants")
    added_by = models.ForeignKey("users.User", on_delete=models.CASCADE, related_name="added_participants")
    last_read_at = models.DateTimeField(blank=True, null=True, editable=False)
    received_at = models.DateTimeField(blank=True, null=True, editable=False)

    class Meta:
        indexes = [models.Index(fields=["role", "letter"])]

    @property
    def has_read(self) -> bool:
        return True if self.last_read_at else False

    def clean(self):
        author_count = BaseParticipant.objects.filter(letter=self.letter, role=self.Roles.AUTHOR).count()

        if author_count != 1:
            raise ValidationError(_("The letter must have exactly one designated author."))

        primary_recipient_count = BaseParticipant.objects.filter(
            letter=self.letter,
            role=self.Roles.PRIMARY_RECIPIENT,
        ).count()

        if primary_recipient_count == 0:
            raise ValidationError(_("There should be at least one primary recipient assigned to the letter."))

    def save(self, *args, **kwargs):
        if self.role == self.Roles.AUTHOR:
            existing_author_count = BaseParticipant.objects.filter(letter=self.letter, role=self.Roles.AUTHOR).count()
            if existing_author_count > 1:
                raise ValidationError({"role": _("There can only be one author per letter.")})

        if self.role == self.Roles.ADMINISTRATOR:
            existing_admin_count = BaseParticipant.objects.filter(
                letter=self.letter,
                role=self.Roles.ADMINISTRATOR,
            ).count()
            if existing_admin_count > 0:
                raise ValidationError({"role": _("There can only be one administrator per letter.")})

        super().save(*args, **kwargs)


class InternalUserParticipant(BaseParticipant):
    user = models.ForeignKey("users.User", on_delete=models.CASCADE, related_name="participated_in_letters")

    def save(self, *args, **kwargs):
        if isinstance(self.letter, Outgoing) and self.role == BaseParticipant.Roles.PRIMARY_RECIPIENT:
            raise ValidationError("Internal users cannot be primary recipients of outgoing letters.")

        permissions = kwargs.pop("permissions", None)

        super().save(*args, **kwargs)
        assign_permissions(
            letter_instance=self.letter,
            participant_user=self.user,
            participant_role=self.role,
            permissions=permissions,
        )

    def delete(self, *args, **kwargs):
        remove_permissions(
            letter_instance=self.letter,
            participant_user=self.user,
            participant_role=self.role,
        )

        super().delete(*args, **kwargs)


class PublicEnterpriseParticipant(BaseParticipant):
    user = models.ForeignKey(
        "enterprises.PublicEnterprise",
        on_delete=models.CASCADE,
        related_name="pub_referenced_in_letters",
    )

    def save(self, *args, **kwargs):
        if isinstance(self.letter, Internal):
            raise ValidationError("Public enterprises cannot participate in internal letters.")

        super().save(*args, **kwargs)


class ExternalUserParticipant(BaseParticipant):
    user = models.ForeignKey("contacts.Contact", on_delete=models.CASCADE, related_name="contact_referenced_in_letters")

    def save(self, *args, **kwargs):
        if isinstance(self.letter, Internal):
            raise ValidationError("External users cannot participate in internal letters.")

        super().save(*args, **kwargs)
