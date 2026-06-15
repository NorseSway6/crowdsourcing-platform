from django.contrib import admin

from app.db.models.pool import Pool, PoolInstruction


@admin.register(Pool)
class PoolAdmin(admin.ModelAdmin):
    list_display = ["pool_id", "tasks_limit", "pipeline", "points", "overlap", "created_at", "pool_type", "status"]


@admin.register(PoolInstruction)
class PoolInstructionAdmin(admin.ModelAdmin):
    list_display = ["id", "title"]
