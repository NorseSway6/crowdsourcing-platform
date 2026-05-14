from django.contrib import admin

from app.presentation.admin.admin_user import AdminUserAdmin
from app.presentation.admin.assignments import AssignmentAdmin
from app.presentation.admin.audit_log import AuditLogAdmin
from app.presentation.admin.dataset import DatasetAdmin
from app.presentation.admin.platform_user import PlatformUserAdmin
from app.presentation.admin.pool import PoolAdmin
from app.presentation.admin.skill import SkillAdmin
from app.presentation.admin.task import TaskAdmin
from app.presentation.admin.user_profile import UserProfileAdmin

admin.site.site_title = "Crowdsourcing Platform"
admin.site.site_header = "Crowdsourcing Platform"
