from django.contrib import admin

from app.internal.models.platform_user import PlatformUser


@admin.register(PlatformUser)
class PlatformUserAdmin(admin.ModelAdmin):
    list_display = ["user_id", "email", "role", "created_at", "is_active"]
