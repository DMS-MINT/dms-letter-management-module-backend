from django.db import models
from django.utils.translation import gettext_lazy as _

from core.letters.models import Letter


class WorkflowLog(models.Model):
    actor = models.ForeignKey(
        "users.User",
        on_delete=models.CASCADE,
        related_name="workflow_logs",
        verbose_name=_("User"),
    )
    action = models.CharField(max_length=50, verbose_name=_("Action"))
    resource = models.ForeignKey(Letter, on_delete=models.CASCADE, max_length=255, verbose_name=_("Resource"))
    role = models.CharField(max_length=50, verbose_name=_("Role"))
    initial_state = models.IntegerField(_("Initial State"), choices=Letter.States.choices)
    final_state = models.IntegerField(_("Final State"), choices=Letter.States.choices)
    timestamp = models.DateTimeField(auto_now_add=True, verbose_name=_("Timestamp"))
    success = models.BooleanField(verbose_name=_("Success"))

    class Meta:
        verbose_name = _("Workflow Log")
        verbose_name_plural = _("Workflow Logs")
        ordering = ["-timestamp"]

    def __str__(self):
        return f"WorkflowLog: {self.user} performed {self.action} on {self.resource}"
