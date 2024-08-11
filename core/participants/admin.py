from django.contrib import admin
from polymorphic.admin import (
    PolymorphicChildModelAdmin,
    PolymorphicChildModelFilter,
    PolymorphicParentModelAdmin,
)

from .models import BaseParticipant, ExternalUserParticipant, InternalUserParticipant, PublicEnterpriseParticipant


class ParticipantChildAdmin(PolymorphicChildModelAdmin):
    base_model = BaseParticipant
    list_display: list[str] = ("role", "letter")


@admin.register(InternalUserParticipant)
class InternalParticipantAdmin(ParticipantChildAdmin):
    base_model = InternalUserParticipant
    show_in_index = True


@admin.register(PublicEnterpriseParticipant)
class PublicEnterpriseParticipantAdmin(ParticipantChildAdmin):
    base_model = PublicEnterpriseParticipant
    show_in_index = True


@admin.register(ExternalUserParticipant)
class ExternalUserParticipantAdmin(ParticipantChildAdmin):
    base_model = ExternalUserParticipant
    show_in_index = True


@admin.register(BaseParticipant)
class BaseParticipantAdmin(PolymorphicParentModelAdmin):
    base_model: BaseParticipant
    list_display: list[str] = ("role", "letter")
    child_models = (InternalUserParticipant, PublicEnterpriseParticipant, ExternalUserParticipant)
    list_filter = (PolymorphicChildModelFilter,)
