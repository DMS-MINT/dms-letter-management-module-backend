from django.contrib import admin

from .models import Email
from .services import email_send_all


@admin.register(Email)
class EmailAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "subject",
        "to",
        "status",
        "sent_at",
    ]
    actions = ["send_email"]

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        return queryset.defer("html", "plain_text")

    @admin.action(description="Send selected emails.")
    def send_email(self, request, queryset):
        email_send_all(queryset)
