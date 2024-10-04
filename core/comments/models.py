from django.conf import settings
from django.db import models
from django.utils.translation import gettext_lazy as _

from core.common.models import BaseModel


class Comment(BaseModel):
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="comments",
        verbose_name=_("Author"),
    )
    message = models.TextField(verbose_name=_("Content"))
    letter = models.ForeignKey(
        "letters.Letter",
        on_delete=models.CASCADE,
        related_name="comments",
        verbose_name=_("Letter"),
    )

    class Meta:
        verbose_name = _("Comment")
        verbose_name_plural = _("Comments")
        ordering = ["-created_at"]

    def __str__(self):
        return f"Comment by {self.author} on {self.letter}"
