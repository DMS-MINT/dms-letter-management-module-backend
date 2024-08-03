from django.contrib import admin

from .models import LetterAttachment


@admin.register(LetterAttachment)
class AttachmentAdmin(admin.ModelAdmin):
    list_display = ("get_letter_reference_number", "remote_file_url", "uploaded_file", "uploaded_by")

    def get_letter_reference_number(self, instance):
        return instance.letter.reference_number
