from django.contrib import admin

from app.db.models.skill import Skill


@admin.register(Skill)
class SkillAdmin(admin.ModelAdmin):
    list_display = ["name"]
