from django.contrib import admin

from app.internal.models.task import Task


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ["task_id", "dataset", "image", "current_stage", "status", "created_at"]
