from enum import Enum

import django_filters
from django.db.models import Q

from core.participants.models import Participant

from .models import Letter


class LetterCategory(Enum):
    INBOX = "inbox/"
    OUTBOX = "outbox/"
    DRAFT = "draft/"


class LetterState(Enum):
    PENDING = "pending/"
    PUBLISHED = "published/"


# Filter class for filtering Letter objects based on different categories like inbox, outbox, or draft.
class BaseLetterFilter(django_filters.FilterSet):
    category = django_filters.CharFilter(method="filter_by_category")

    def __init__(self, data=None, queryset=None, *, current_user=None, **kwargs):
        super().__init__(data, queryset, **kwargs)
        self.current_user = current_user

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

    def filter_inbox(self, queryset):
        current_state_filter = Q(
            current_state__in=[
                Letter.States.PUBLISHED,
                Letter.States.CLOSED,
            ],
        )

        participant_filter = Q(
            participants__user_id=self.current_user.id,
            participants__role__in=[
                Participant.Roles.PRIMARY_RECIPIENT,
                Participant.Roles.CC,
                Participant.Roles.BCC,
                Participant.Roles.COLLABORATOR,
            ],
        )

        combined_filter = current_state_filter & participant_filter

        return queryset.filter(combined_filter)

    def filter_outbox(self, queryset):
        current_state_filter = Q(
            current_state__in=[
                Letter.States.SUBMITTED,
                Letter.States.PUBLISHED,
                Letter.States.CLOSED,
            ],
        )

        participant_filter = Q(
            participants__user_id=self.current_user.id,
            participants__role__in=[
                Participant.Roles.AUTHOR,
                Participant.Roles.EDITOR,
            ],
        )

        combined_filter = current_state_filter & participant_filter

        return queryset.filter(combined_filter)

    def filter_draft(self, queryset):
        current_state_filter = Q(
            current_state__in=[
                Letter.States.DRAFT,
            ],
        )

        participant_filter = Q(
            participants__user_id=self.current_user.id,
            participants__role__in=[
                Participant.Roles.AUTHOR,
                Participant.Roles.EDITOR,
                Participant.Roles.COLLABORATOR,
            ],
        )

        combined_filter = current_state_filter & participant_filter

        return queryset.filter(combined_filter)
