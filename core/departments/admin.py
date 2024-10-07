from django.contrib import admin

from .models import Department


@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = (
        "department_name_en",
        "department_name_am",
        "abbreviation_en",
        "abbreviation_am",
        "created_at",
        "updated_at",
    )
    ordering = ["department_name_en"]
