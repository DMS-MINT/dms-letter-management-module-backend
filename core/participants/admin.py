from django.contrib import admin

from .models import Participant, Role


@admin.register(Participant)
class ParticipantAdmin(admin.ModelAdmin):
    list_display: list[str] = ["user", "role", "letter"]


@admin.register(Role)
class RoleAdmin(admin.ModelAdmin):
    list_display: list[str] = ["name", "permissions"]
