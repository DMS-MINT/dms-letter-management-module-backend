from django.core.exceptions import ValidationError
from django.db import models
from django.utils.translation import gettext_lazy as _

from core.common.models import BaseModel
from core.letters.models import Letter
from core.permissions.service import assign_permissions, remove_permissions
from core.users.models import User


class Participant(BaseModel):
    class Roles(models.IntegerChoices):
        AUTHOR = 1, _("Author")
        PRIMARY_RECIPIENT = 2, _("Primary Recipient")
        CC = 3, _("Carbon Copy Recipient")
        BCC = 4, _("Blind Carbon Copy Recipient")
        COLLABORATOR = 5, _("Collaborator")
        ADMINISTRATOR = 6, _("Administrator")

    role = models.IntegerField(choices=Roles.choices, verbose_name=_("Roles"))
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="participates_in")
    letter = models.ForeignKey(Letter, on_delete=models.CASCADE, related_name="participants")
    added_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name="added_participants")
    last_read_at = models.DateTimeField(blank=True, null=True, editable=False)
    received_at = models.DateTimeField(blank=True, null=True, editable=False)

    @property
    def has_read(self) -> bool:
        return True if self.last_read_at else False

    def clean(self):
        author_count = Participant.objects.filter(letter=self.letter, role=self.Roles.AUTHOR).count()

        if author_count != 1:
            raise ValidationError(_("The letter must have exactly one designated author."))

        primary_recipient_count = Participant.objects.filter(
            letter=self.letter,
            role=self.Roles.PRIMARY_RECIPIENT,
        ).count()

        if primary_recipient_count == 0:
            raise ValidationError(_("There should be at least one primary recipient assigned to the letter."))

    def save(self, *args, **kwargs):
        if self.role == self.Roles.AUTHOR:
            existing_author_count = Participant.objects.filter(letter=self.letter, role=self.Roles.AUTHOR).count()
            if existing_author_count > 1:
                raise ValidationError({"role": _("There can only be one author per letter.")})

        if self.role == self.Roles.ADMINISTRATOR:
            existing_admin_count = Participant.objects.filter(letter=self.letter, role=self.Roles.ADMINISTRATOR).count()
            if existing_admin_count > 0:
                raise ValidationError({"role": _("There can only be one administrator per letter.")})

        permissions = kwargs.pop("permissions", None)

        super().save(*args, **kwargs)
        if isinstance(self.user, User):
            assign_permissions(
                letter_instance=self.letter,
                participant_user=self.user,
                participant_role=self.role,
                permissions=permissions,
            )

    def delete(self, *args, **kwargs):
        if isinstance(self.user, User):
            remove_permissions(
                letter_instance=self.letter,
                participant_user=self.user,
                participant_role=self.role,
            )

        super().delete(*args, **kwargs)

    class Meta:
        verbose_name: str = _("Participant")
        verbose_name_plural: str = _("Participants")
        unique_together = [["user", "letter"]]
