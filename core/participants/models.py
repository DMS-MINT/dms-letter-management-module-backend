from django.db import models
from django.utils.translation import gettext_lazy as _

from core.common.models import BaseModel
from core.letters.models import Letter
from core.permissions.models import Permission
from core.users.models import BaseUser


class Participant(BaseModel):
    class RoleNames(models.IntegerChoices):
        EDITOR = 1, _("Editor")
        AUTHOR = 2, _("Author")
        PRIMARY_RECIPIENT = 3, _("Primary Recipient")
        CC = 4, _("Carbon Copy Recipient")
        BCC = 5, _("Blind Carbon Copy Recipient")
        COLLABORATOR = 6, _("Collaborator")

    role_name = models.IntegerField(
        _("Role Name"),
        choices=RoleNames.choices,
        help_text=_("Select the role name of this participant."),
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
    permissions = models.ManyToManyField(Permission)

    last_read_at = models.DateTimeField(blank=True, null=True, editable=False)
    received_at = models.DateTimeField(blank=True, null=True, editable=False)

    _dirty = True
    _current_user = None

    @property
    def has_read(self) -> bool:
        return True if self.last_read_at else False

    def can(self, action):
        return self.permissions.filter(name=action).exists()

    def save(self, *args, **kwargs):
        self._current_user = kwargs.pop("current_user", None)
        super().save(*args, **kwargs)

    class Meta:
        verbose_name: str = _("Participant")
        verbose_name_plural: str = _("Participants")
        unique_together = [["user", "letter"]]
