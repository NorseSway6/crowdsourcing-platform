from django.contrib import admin

from app.internal.models.dataset import Dataset


@admin.register(Dataset)
class DatasetAdmin(admin.ModelAdmin):
    list_display = ["dataset_id", "name", "domain", "owner", "created_at"]
