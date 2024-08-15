from django.contrib import admin

from .models import InAppNotification


@admin.register(InAppNotification)
class InAppNotificationAdmin(admin.ModelAdmin):
    list_display = ("status", "sender", "is_read", "is_notified", "sent_at")
    ordering = ("sent_at",)
    search_fields = ("status", "sender__username")
    list_filter = ("status", "is_read", "is_notified")
    readonly_fields = ("sent_at",)
