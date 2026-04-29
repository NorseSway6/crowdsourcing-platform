from django.contrib import admin

from app.db.models.user_profile import UserProfile


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ["user", "first_name", "last_name", "middle_name", "group", "institution"]
