from django.contrib import admin

from .models import Participant


@admin.register(Participant)
class Admin(admin.ModelAdmin):
    list_display: list[str] = ["user", "role", "letter"]
