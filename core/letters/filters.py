from enum import Enum

import django_filters
from django.contrib.contenttypes.models import ContentType
from django.db.models import Q

from core.participants.models import BaseParticipant, InternalUserParticipant

from .models import Letter


class LetterCategory(Enum):
    INBOX = "inbox"
    OUTBOX = "outbox"
    DRAFT = "draft"
    PENDING = "pending"
    PUBLISHED = "published"
    TRASH = "trash"


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
        match value:
            case LetterCategory.INBOX.value:
                return self.filter_inbox(queryset)
            case LetterCategory.OUTBOX.value:
                return self.filter_outbox(queryset)
            case LetterCategory.DRAFT.value:
                return self.filter_draft(queryset)
            case LetterCategory.TRASH.value:
                return self.filter_trash(queryset)
            case LetterCategory.PENDING.value:
                if self.current_user.is_staff:
                    return self.filter_pending(queryset)
                return queryset.none()
            case LetterCategory.PUBLISHED.value:
                if self.current_user.is_staff:
                    return self.filter_published(queryset)
                return queryset.none()
            case _:
                return queryset.none()

    def filter_inbox(self, queryset):
        current_state_filter = Q(
            current_state__in=[
                Letter.States.PUBLISHED,
                Letter.States.CLOSED,
            ],
        )

        internal_user_ct = ContentType.objects.get_for_model(InternalUserParticipant)

        participant_filter = Q(
            participants__polymorphic_ctype=internal_user_ct,
            participants__internaluserparticipant__user_id=self.current_user.id,
            participants__role__in=[
                BaseParticipant.Roles.PRIMARY_RECIPIENT,
                BaseParticipant.Roles.CC,
                BaseParticipant.Roles.BCC,
                BaseParticipant.Roles.COLLABORATOR,
            ],
        )

        combined_filter = current_state_filter & participant_filter

        return queryset.filter(combined_filter).distinct()

    def filter_outbox(self, queryset):
        current_state_filter = Q(
            current_state__in=[
                Letter.States.SUBMITTED,
                Letter.States.PUBLISHED,
                Letter.States.CLOSED,
            ],
        )
        internal_user_ct = ContentType.objects.get_for_model(InternalUserParticipant)

        participant_filter = Q(
            participants__polymorphic_ctype=internal_user_ct,
            participants__internaluserparticipant__user_id=self.current_user.id,
            participants__role__in=[
                BaseParticipant.Roles.AUTHOR,
                BaseParticipant.Roles.COLLABORATOR,
            ],
        )

        combined_filter = current_state_filter & participant_filter

        return queryset.filter(combined_filter).distinct()

    def filter_draft(self, queryset):
        current_state_filter = Q(
            current_state__in=[
                Letter.States.DRAFT,
                Letter.States.REJECTED,
            ],
        )

        internal_user_ct = ContentType.objects.get_for_model(InternalUserParticipant)

        participant_filter = Q(
            current_state_filter,
            participants__polymorphic_ctype=internal_user_ct,
            participants__internaluserparticipant__user_id=self.current_user.id,
            participants__role__in=[
                BaseParticipant.Roles.AUTHOR,
                BaseParticipant.Roles.COLLABORATOR,
            ],
        )

        owner_filter = Q(
            current_state_filter,
            owner=self.current_user.id,
        )

        combined_filter = current_state_filter & (participant_filter | owner_filter)

        return queryset.filter(combined_filter).distinct()

    def filter_trash(self, queryset):
        current_state_filter = Q(current_state__in=[Letter.States.TRASHED])

        internal_user_ct = ContentType.objects.get_for_model(InternalUserParticipant)

        participant_filter = Q(
            participants__polymorphic_ctype=internal_user_ct,
            participants__internaluserparticipant__user_id=self.current_user.id,
            participants__role__in=[BaseParticipant.Roles.AUTHOR],
        )

        combined_filter = current_state_filter & participant_filter

        return queryset.filter(combined_filter).distinct()

    def filter_pending(self, queryset):
        current_state_filter = Q(
            current_state__in=[Letter.States.SUBMITTED],
        )

        internal_user_ct = ContentType.objects.get_for_model(InternalUserParticipant)

        participant_filter = ~Q(
            participants__polymorphic_ctype=internal_user_ct,
            participants__internaluserparticipant__user_id=self.current_user.id,
            participants__role__in=[
                BaseParticipant.Roles.AUTHOR,
                BaseParticipant.Roles.PRIMARY_RECIPIENT,
                BaseParticipant.Roles.BCC,
                BaseParticipant.Roles.CC,
                BaseParticipant.Roles.COLLABORATOR,
            ],
        )

        combined_filter = current_state_filter & participant_filter

        return queryset.filter(combined_filter).exclude(owner=self.current_user).distinct()

    def filter_published(self, queryset):
        current_state_filter = Q(
            current_state__in=[Letter.States.PUBLISHED],
        )

        combined_filter = current_state_filter

        return queryset.filter(combined_filter).distinct()
