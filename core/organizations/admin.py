from django.contrib import admin
from django_tenants.admin import TenantAdminMixin

from .models import Organization


@admin.register(Organization)
class OrganizationAdmin(TenantAdminMixin, admin.ModelAdmin):
    list_display = ("name",)
