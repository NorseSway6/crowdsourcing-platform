from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from app.db.models.admin_user import AdminUser


@admin.register(AdminUser)
class AdminUserAdmin(UserAdmin):
    list_display = ["id", "username", "email"]
