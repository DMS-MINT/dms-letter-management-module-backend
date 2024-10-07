from django.contrib import admin

from .models import JobTitle


@admin.register(JobTitle)
class JobTitleAdmin(admin.ModelAdmin):
    list_display = ("title_en", "title_am", "created_at", "updated_at")
    ordering = ["title_en"]
