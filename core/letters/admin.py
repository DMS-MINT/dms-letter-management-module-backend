from django.contrib import admin
from django.utils.html import format_html
from polymorphic.admin import (
    PolymorphicChildModelAdmin,
    PolymorphicChildModelFilter,
    PolymorphicParentModelAdmin,
)

# from core.participants.models import Participant
from .models import Incoming, Internal, Letter, Outgoing

# class ParticipantInline(admin.StackedInline):
#     model = Participant
#     extra = 1


class LetterChildAdmin(PolymorphicChildModelAdmin):
    base_model = Letter
    list_display: list[str] = [
        "reference_number",
        "current_state",
        "created_at",
        "updated_at",
        "pdf_view_link",
        "hidden",
    ]
    # inlines = [ParticipantInline]
    ordering = ["-updated_at"]
    readonly_fields = ["reference_number", "pdf_version"]

    def pdf_view_link(self, obj):
        if obj.pdf_version:
            return format_html('<a href="{}" target="_blank">View PDF</a>', obj.pdf_version)
        return "-"

    pdf_view_link.short_description = "PDF Version"


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
    list_display: list[str] = [
        "reference_number",
        "current_state",
        "created_at",
        "updated_at",
        "pdf_view_link",
    ]
    child_models = (Internal, Incoming, Outgoing)
    list_filter = (PolymorphicChildModelFilter,)
    ordering = ["-updated_at"]
    readonly_fields = ["reference_number", "pdf_version"]

    def pdf_view_link(self, obj):
        if obj.pdf_version:
            return format_html('<a href="{}" target="_blank">View PDF</a>', obj.pdf_version)
        return "-"

    pdf_view_link.short_description = "PDF Version"
