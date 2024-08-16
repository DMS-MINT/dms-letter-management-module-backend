from django.urls import path
from django.urls.resolvers import URLPattern

from .apis import (
    BulkMarkNotificationAsRead,
    MarkNotificationAsNotified,
    MarkNotificationAsRead,
    NotificationListApi,
    SendReminderApi,
)

app_name = "notifications"

urlpatterns: list[URLPattern] = [
    path("", NotificationListApi.as_view(), name="notifications-list"),
    path("<uuid:notification_id>/read/", MarkNotificationAsRead.as_view(), name="notifications-read"),
    path("<uuid:notification_id>/notified/", MarkNotificationAsNotified.as_view(), name="notifications-notified"),
    path("bulk/read/", BulkMarkNotificationAsRead.as_view(), name="notifications-bulk-read"),
    path("reminder/", SendReminderApi.as_view(), name="notifications-reminder"),
]
