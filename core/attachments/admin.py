from django.contrib import admin

from .models import Attachment


@admin.register(Attachment)
class AttachmentAdmin(admin.ModelAdmin):
    list_display = ["get_letter_reference_number", "file", "description", "created_at"]

    def get_letter_reference_number(self, instance):
        return instance.letter.reference_number
