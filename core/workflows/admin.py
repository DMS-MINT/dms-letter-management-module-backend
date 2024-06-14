from django.contrib import admin

from .models import WorkflowLog


@admin.register(WorkflowLog)
class WorkflowLogAdmin(admin.ModelAdmin):
    list_display = ["user", "action", "resource", "initial_state", "final_state", "timestamp", "success"]
