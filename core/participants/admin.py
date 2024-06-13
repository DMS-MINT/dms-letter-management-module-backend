from django.contrib import admin

from .models import Participant


@admin.register(Participant)
class ParticipantAdmin(admin.ModelAdmin):
    list_display: list[str] = ["role_name", "user", "letter", "display_permissions"]

    def display_permissions(self, obj):
        return ", ".join([permission.action for permission in obj.permissions.all()])
