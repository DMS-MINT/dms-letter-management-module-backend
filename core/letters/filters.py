from enum import Enum

import django_filters
from django.db.models import Q

from core.participants.models import Participant

from .models import Letter, State


class LetterCategory(Enum):
    INBOX = "inbox"
    OUTBOX = "outbox"
    DRAFT = "draft"


# Filter class for filtering Letter objects based on different categories like inbox, outbox, or draft.
class BaseLetterFilter(django_filters.FilterSet):
    category = django_filters.CharFilter(method="filter_by_category")

    class Meta:
        model = Letter
        fields = []

    def filter_by_category(self, queryset, name, value):
        if value == LetterCategory.INBOX.value:
            return self.filter_inbox(queryset)

        if value == LetterCategory.OUTBOX.value:
            return self.filter_outbox(queryset)

        if value == LetterCategory.DRAFT.value:
            return self.filter_draft(queryset)

        return queryset.none()

    @staticmethod
    def filter_inbox(queryset):
        return queryset.filter(
            Q(
                current_state__in=[
                    State.objects.get(name="Published"),
                    State.objects.get(name="closed"),
                ],
            )
            & Q(
                participants__role_name__in=[
                    Participant.RoleNames.PRIMARY_RECIPIENT,
                    Participant.RoleNames.CC,
                    Participant.RoleNames.BCC,
                    Participant.RoleNames.COLLABORATOR,
                ],
            ),
        )

    @staticmethod
    def filter_outbox(queryset):
        return queryset.filter(
            Q(
                current_state__in=[
                    State.objects.get(name="Submitted"),
                    State.objects.get(name="Published"),
                    State.objects.get(name="Closed"),
                ],
            )
            & Q(
                participants__role_name__in=[
                    Participant.RoleNames.AUTHOR,
                    Participant.RoleNames.COLLABORATOR,
                ],
            ),
        )

    @staticmethod
    def filter_draft(queryset):
        return queryset.filter(
            Q(
                current_state__in=[
                    State.objects.get(name="Draft"),
                ],
            )
            & Q(
                participants__role_name__in=[
                    Participant.RoleNames.AUTHOR,
                    Participant.RoleNames.EDITOR,
                    Participant.RoleNames.COLLABORATOR,
                ],
            ),
        )
