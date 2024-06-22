from django.db import models
from django.utils.translation import gettext_lazy as _

from core.common.models import BaseModel
from core.letters.models import Letter
from core.users.models import BaseUser, Member


class Participant(BaseModel):
    class Roles(models.IntegerChoices):
        AUTHOR = 1, _("Author")
        PRIMARY_RECIPIENT = 2, _("Primary Recipient")
        CC = 3, _("Carbon Copy Recipient")
        BCC = 4, _("Blind Carbon Copy Recipient")
        COLLABORATOR = 5, _("Collaborator")
        ADMINISTRATOR = 6, _("Administrator")

    role = models.IntegerField(
        _("Roles"),
        choices=Roles.choices,
        help_text=_("Select the role of this participant."),
    )
    user = models.ForeignKey(
        BaseUser,
        on_delete=models.CASCADE,
        related_name="participates_in",
        help_text=_("Select the user associated with this participant."),
    )
    letter = models.ForeignKey(
        Letter,
        on_delete=models.CASCADE,
        related_name="participants",
        help_text=_("Select the letter associated with this participant."),
    )
    added_by = models.ForeignKey(Member, on_delete=models.CASCADE, related_name="added_participants")
    last_read_at = models.DateTimeField(blank=True, null=True, editable=False)
    received_at = models.DateTimeField(blank=True, null=True, editable=False)

    @property
    def has_read(self) -> bool:
        return True if self.last_read_at else False

    class Meta:
        verbose_name: str = _("Participant")
        verbose_name_plural: str = _("Participants")
        unique_together = [["user", "letter"]]
