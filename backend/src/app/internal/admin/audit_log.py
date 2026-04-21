from django.contrib import admin

from app.internal.models.audit_log import AuditLog


@admin.register(AuditLog)
class AuditLogAdmin(admin.ModelAdmin):
    list_display = ["audit_id", "user", "task", "action", "timestamp", "ip_address"]
