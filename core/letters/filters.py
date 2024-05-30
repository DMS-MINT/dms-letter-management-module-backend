from enum import Enum

import django_filters
from django.db.models import Q

from core.participants.models import Participant

from .models import Letter


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
                status__in=[
                    Letter.LetterStatus.COMPLETED,
                    Letter.LetterStatus.FORWARDED_PENDING_REVIEW,
                    Letter.LetterStatus.FORWARDED_UNDER_REVIEW,
                    Letter.LetterStatus.FORWARDED_REVIEWED,
                    Letter.LetterStatus.PUBLISHED,
                ],
            )
            & Q(
                participants__role__in=[
                    Participant.Roles.BCC,
                    Participant.Roles.CC,
                    Participant.Roles.RECIPIENT,
                ],
            ),
        )

    @staticmethod
    def filter_outbox(queryset):
        return queryset.filter(
            Q(
                status__in=[
                    Letter.LetterStatus.COMPLETED,
                    Letter.LetterStatus.FORWARDED_PENDING_REVIEW,
                    Letter.LetterStatus.FORWARDED_UNDER_REVIEW,
                    Letter.LetterStatus.FORWARDED_REVIEWED,
                    Letter.LetterStatus.PENDING_APPROVAL,
                    Letter.LetterStatus.PUBLISHED,
                ],
            )
            & Q(
                participants__role__in=[
                    Participant.Roles.SENDER,
                ],
            ),
        )

    @staticmethod
    def filter_draft(queryset):
        return queryset.filter(
            Q(
                status__in=[
                    Letter.LetterStatus.CANCELLED,
                    Letter.LetterStatus.DRAFT,
                    Letter.LetterStatus.DRAFT_PENDING_REVIEW,
                    Letter.LetterStatus.DRAFT_REVIEWED,
                    Letter.LetterStatus.DRAFT_UNDER_REVIEW,
                ],
            )
            & Q(
                participants__role__in=[
                    Participant.Roles.DRAFTER,
                    Participant.Roles.DRAFT_REVIEWER,
                    Participant.Roles.SENDER,
                ],
            ),
        )
