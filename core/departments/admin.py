from django.contrib import admin

from .models import Department


@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ("name_en", "name_am", "created_at", "updated_at")
    ordering = ["name_en"]
