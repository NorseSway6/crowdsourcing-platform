from django.contrib import admin

from app.internal.admin.admin_user import AdminUserAdmin
from app.internal.admin.assignments import AssignmentAdmin
from app.internal.admin.audit_log import AuditLogAdmin
from app.internal.admin.dataset import DatasetAdmin
from app.internal.admin.platform_user import PlatformUserAdmin
from app.internal.admin.task import TaskAdmin

admin.site.site_title = "Crowdsourcing Platform"
admin.site.site_header = "Crowdsourcing Platform"
