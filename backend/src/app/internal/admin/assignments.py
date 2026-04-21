from django.contrib import admin

from app.internal.models.assignments import Assignment


@admin.register(Assignment)
class AssignmentAdmin(admin.ModelAdmin):
    list_display = ["assignment_id", "task", "user", "stage", "verdict", "started_at", "completed_at"]
