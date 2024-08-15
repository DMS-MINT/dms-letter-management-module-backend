from django.contrib import admin

from .models import InApp, Tag


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ("name",)
    ordering = ("name",)
    search_fields = ("name",)
    list_filter = ("name",)
    list_display_links = ("name",)


@admin.register(InApp)
class InAppAdmin(admin.ModelAdmin):
    list_display = ("status", "sender", "to", "is_read", "is_notified", "sent_at")
    ordering = ("sent_at",)
    search_fields = ("status", "sender__username", "to__username")
    list_filter = ("status", "is_read", "is_notified")
    readonly_fields = ("sent_at",)
