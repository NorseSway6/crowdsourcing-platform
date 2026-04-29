from django.contrib import admin

from app.db.models.task import Task


@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ["task_id", "pool", "dataset", "image_url", "created_at"]
