from django.db import models
from django.utils.translation import gettext_lazy as _

from core.letters.models import Letter, State
from core.permissions.models import Permission
from core.users.models import Member


class WorkflowLog(models.Model):
    user = models.ForeignKey(
        Member,
        on_delete=models.CASCADE,
        related_name="access_logs",
        verbose_name=_("User"),
        help_text=_("The user who performed the action."),
    )
    action = models.ForeignKey(
        Permission,
        on_delete=models.CASCADE,
        verbose_name=_("Action"),
        help_text=_("The action that was performed."),
    )
    resource = models.ForeignKey(
        Letter,
        on_delete=models.CASCADE,
        max_length=255,
        verbose_name=_("Resource"),
        help_text=_("The resource that was accessed or modified."),
    )
    role = models.CharField(
        max_length=50,
        verbose_name=_("Role"),
        help_text=_("The role of the user at the time of the action."),
    )
    initial_state = models.ForeignKey(
        State,
        on_delete=models.CASCADE,
        verbose_name=_("Initial State"),
        help_text=_("The state of the resource before the action was performed."),
    )
    final_state = models.ForeignKey(
        State,
        on_delete=models.CASCADE,
        verbose_name=_("Final State"),
        help_text=_("The state of the resource after the action was performed."),
    )
    timestamp = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_("Timestamp"),
        help_text=_("The date and time when the action was performed."),
    )
    success = models.BooleanField(
        verbose_name=_("Success"),
        help_text=_("Indicates whether the action was successful."),
    )

    class Meta:
        verbose_name = _("Access Log")
        verbose_name_plural = _("Access Logs")
        ordering = ["-timestamp"]

    def __str__(self):
        return f"WorkflowLog: {self.user} performed {self.action} on {self.resource}"
