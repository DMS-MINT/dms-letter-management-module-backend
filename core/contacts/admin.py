from django.contrib import admin

from .models import Contact


@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ("full_name_en", "full_name_am", "address", "email", "phone_number")
    search_fields = ("full_name_en", "full_name_am", "email")
    ordering = ("full_name_en",)
