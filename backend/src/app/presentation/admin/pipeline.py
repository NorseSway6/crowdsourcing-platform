from django.contrib import admin

from app.db.models.pipeline import Pipeline


@admin.register(Pipeline)
class PipelineAdmin(admin.ModelAdmin):
    list_display = ["pipeline_id", "name", "dataset", "limit", "owner", "created_at"]
