from django.contrib import admin
from polymorphic.admin import (
    PolymorphicChildModelAdmin,
    PolymorphicChildModelFilter,
    PolymorphicParentModelAdmin,
)

from core.participants.models import Participant

from .models import Incoming, Internal, Letter, Outgoing


class ParticipantInline(admin.StackedInline):
    model = Participant
    extra = 1


class LetterChildAdmin(PolymorphicChildModelAdmin):
    base_model = Letter
    list_display: list[str] = ["subject", "content", "status", "created_at"]
    inlines = [ParticipantInline]


@admin.register(Internal)
class InternalAdmin(LetterChildAdmin):
    base_model = Internal
    show_in_index = True


@admin.register(Incoming)
class IncomingAdmin(LetterChildAdmin):
    base_model = Incoming
    show_in_index = True


@admin.register(Outgoing)
class OutgoingAdmin(LetterChildAdmin):
    base_model = Outgoing
    show_in_index = True


@admin.register(Letter)
class LetterParentAdmin(PolymorphicParentModelAdmin):
    base_model = Letter
    list_display: list[str] = ["subject", "content", "status", "created_at"]
    child_models = (Internal, Incoming, Outgoing)
    list_filter = (PolymorphicChildModelFilter,)
