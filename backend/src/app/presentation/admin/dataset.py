from django.contrib import admin

from app.db.models.dataset import Dataset, DatasetCategory


@admin.register(Dataset)
class DatasetAdmin(admin.ModelAdmin):
    list_display = ["dataset_id", "name", "domain", "owner", "created_at"]


@admin.register(DatasetCategory)
class DatasetCategoryAdmin(admin.ModelAdmin):
    list_display = ["id", "name"]
