from django.db import models
from django.utils.translation import gettext_lazy as _

from core.common.models import BaseModel
from core.letters.models import Letter
from core.users.models import BaseUser


class Role(BaseModel):
    name = models.CharField(max_length=255)
    permissions = models.JSONField(default=dict)

    def can(self, action):
        return self.permissions.get(action, False)

    def __str__(self):
        return self.name


class Participant(BaseModel):
    user = models.ForeignKey(
        BaseUser,
        on_delete=models.CASCADE,
        related_name="participates_in",
        help_text=_("Select the user associated with this participant."),
    )
    role = models.ForeignKey(
        Role,
        on_delete=models.CASCADE,
        help_text=_("Select the role of this participant."),
    )
    letter = models.ForeignKey(
        Letter,
        on_delete=models.CASCADE,
        related_name="participants",
        help_text=_("Select the letter associated with this participant."),
    )
    last_read_at = models.DateTimeField(blank=True, null=True, editable=False)
    received_at = models.DateTimeField(blank=True, null=True, editable=False)

    @property
    def has_read(self) -> bool:
        return True if self.last_read_at else False

    class Meta:
        verbose_name: str = _("Participant")
        verbose_name_plural: str = _("Participants")
