from django.contrib import admin

from .models import Branch, PublicEnterprise


@admin.register(PublicEnterprise)
class PublicEnterpriseAdmin(admin.ModelAdmin):
    list_display = ("id", "name_en", "name_am", "email", "phone_number")
    search_fields = ("name_en", "name_am", "email")
    ordering = ("name_en",)


@admin.register(Branch)
class BranchAdmin(admin.ModelAdmin):
    list_display = ("id", "enterprise", "address", "phone_number")
    search_fields = ("enterprise__name_en", "address")
    list_filter = ("enterprise",)
    ordering = ("enterprise", "address")
