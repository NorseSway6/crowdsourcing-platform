from django.contrib import admin

from app.db.models.audit_log import AuditLog


@admin.register(AuditLog)
class AuditLogAdmin(admin.ModelAdmin):
    list_display = ["audit_id", "user", "task", "pool", "action", "timestamp", "ip_address"]
