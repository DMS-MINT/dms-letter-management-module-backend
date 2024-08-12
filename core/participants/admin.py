from django.contrib import admin
from polymorphic.admin import (
    PolymorphicChildModelAdmin,
    PolymorphicChildModelFilter,
    PolymorphicParentModelAdmin,
)

from .models import BaseParticipant, EnterpriseParticipant, ExternalUserParticipant, InternalUserParticipant


class ParticipantChildAdmin(PolymorphicChildModelAdmin):
    base_model = BaseParticipant
    list_display: list[str] = ("role", "letter")


@admin.register(InternalUserParticipant)
class InternalParticipantAdmin(ParticipantChildAdmin):
    base_model = InternalUserParticipant
    list_display: list[str] = ("user", "role", "letter")
    show_in_index = True


@admin.register(EnterpriseParticipant)
class EnterpriseParticipantAdmin(ParticipantChildAdmin):
    base_model = EnterpriseParticipant
    list_display: list[str] = ("enterprise", "role", "letter")
    show_in_index = True


@admin.register(ExternalUserParticipant)
class ExternalUserParticipantAdmin(ParticipantChildAdmin):
    base_model = ExternalUserParticipant
    list_display: list[str] = ("contact", "role", "letter")
    show_in_index = True


@admin.register(BaseParticipant)
class BaseParticipantAdmin(PolymorphicParentModelAdmin):
    base_model: BaseParticipant
    list_display: list[str] = ("role", "letter")
    child_models = (InternalUserParticipant, EnterpriseParticipant, ExternalUserParticipant)
    list_filter = (PolymorphicChildModelFilter,)
