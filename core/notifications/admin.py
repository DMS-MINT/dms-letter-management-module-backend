from django.contrib import admin

from .models import ChannelType, Notification, NotificationRecipient, Tag


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ("name",)
    search_fields = ("name",)
    ordering = ("name",)


@admin.register(ChannelType)
class ChannelTypeAdmin(admin.ModelAdmin):
    list_display = ("channel_type",)
    search_fields = ("channel_type",)
    ordering = ("channel_type",)


@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = (
        "subject",
        "status",
        "sent_at",
    )
    search_fields = (
        "subject",
        "message",
    )
    list_filter = (
        "status",
        "channels",
    )
    ordering = ("-sent_at",)
    filter_horizontal = (
        "channels",
        "tags",
    )

    readonly_fields = (
        "status",
        "sent_at",
    )


@admin.register(NotificationRecipient)
class NotificationRecipientAdmin(admin.ModelAdmin):
    list_display = (
        "notification",
        "user",
        "has_read",
        "has_notified",
    )
    search_fields = (
        "user__username",
        "notification__subject",
    )
    list_filter = (
        "has_read",
        "has_notified",
    )
    ordering = ("-notification__sent_at",)

    readonly_fields = (
        "notification",
        "user",
    )
