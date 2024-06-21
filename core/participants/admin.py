from django.contrib import admin

from .models import Participant


@admin.register(Participant)
class ParticipantAdmin(admin.ModelAdmin):
    list_display: list[str] = ["role", "user", "letter"]

    def display_permissions(self, obj):
        return ", ".join([permission.name for permission in obj.permissions.all()])
