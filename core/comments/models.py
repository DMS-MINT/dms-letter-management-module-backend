from django.db import models
from django.utils.translation import gettext_lazy as _

from core.common.models import BaseModel
from core.letters.models import Letter
from core.users.models import Member


class Comment(BaseModel):
    author = models.ForeignKey(
        Member,
        on_delete=models.CASCADE,
        related_name="comments",
        verbose_name=_("Author"),
        help_text=_("Select the user who made this comment."),
    )
    message = models.TextField(
        verbose_name=_("Content"),
        help_text=_("Enter the message of the comment."),
    )
    letter = models.ForeignKey(
        Letter,
        on_delete=models.CASCADE,
        related_name="comments",
        verbose_name=_("Letter"),
        help_text=_("Select the letter associated with this comment."),
    )

    class Meta:
        verbose_name = _("Comment")
        verbose_name_plural = _("Comments")
        ordering = ["-created_at"]

    def __str__(self):
        return f"Comment by {self.author} on {self.letter}"
