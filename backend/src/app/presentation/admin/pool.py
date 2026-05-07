from django.contrib import admin

from app.db.models.pool import Pool


@admin.register(Pool)
class PoolAdmin(admin.ModelAdmin):
    list_display = ["pool_id", "points", "overlap", "created_at", "is_active"]
