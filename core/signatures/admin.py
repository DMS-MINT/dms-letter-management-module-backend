from django.contrib import admin

from .models import LetterSignature, UserDefaultSignature


class SignatureAdmin(admin.ModelAdmin):
    list_display = ("signer", "signature_method", "signature_image")
    search_fields = ("signer__full_name",)
    readonly_fields = ("signature_url", "signer", "signature_method")
    list_filter = ("signature_method",)

    def get_readonly_fields(self, request, obj=None):
        if obj:  # If editing an existing object
            return self.readonly_fields + ("signature_image",)
        return self.readonly_fields

    def signature_url(self, obj):
        if obj.signature_image:
            return obj.signature_url
        return "No signature"

    signature_url.short_description = "Signature URL"


@admin.register(LetterSignature)
class LetterSignatureAdmin(SignatureAdmin):
    list_display = ("letter", "signer", "signature_method", "signature_image")
    search_fields = ("letter__subject", "signer__full_name")
    readonly_fields = SignatureAdmin.readonly_fields + ("letter",)


@admin.register(UserDefaultSignature)
class UserDefaultSignatureAdmin(admin.ModelAdmin):
    list_display = ("user", "signature_image")
    search_fields = ("user__full_name",)
    readonly_fields = ("signature_url",)
    fieldsets = (
        (
            None,
            {
                "fields": (
                    "user",
                    "signature_image",
                ),
            },
        ),
    )

    def get_readonly_fields(self, request, obj=None):
        if obj:  # If editing an existing object
            return self.readonly_fields + ("signature_image",)
        return self.readonly_fields

    def signature_url(self, obj):
        if obj.signature_image:
            return obj.signature_url
        return "No signature"

    signature_url.short_description = "Signature URL"
