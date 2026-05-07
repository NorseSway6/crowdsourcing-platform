from django.contrib import admin

from app.db.models.assignments import Assignment


@admin.register(Assignment)
class AssignmentAdmin(admin.ModelAdmin):
    list_display = ["assignment_id", "task", "user", "started_at", "completed_at", "status"]
