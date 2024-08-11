from django.contrib import admin

from .models import PublicEnterprise


@admin.register(PublicEnterprise)
class PublicEnterpriseAdmin(admin.ModelAdmin):
    list_display = ("name_en", "name_am", "email", "phone_number")
    search_fields = ("name_en", "name_am", "email")
    ordering = ("name_en",)
