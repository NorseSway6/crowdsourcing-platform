from django.db import models

from app.db.models.platform_user import PlatformUser
from app.db.models.skill import Skill


class UserProfile(models.Model):
    user = models.OneToOneField(
        PlatformUser, on_delete=models.CASCADE, related_name="user_profile", verbose_name="user"
    )
    first_name = models.CharField(max_length=30, verbose_name="first_name")
    last_name = models.CharField(max_length=30, verbose_name="last_name")
    middle_name = models.CharField(max_length=30, blank=True, null=True, verbose_name="middle_name")
    group = models.CharField(max_length=15, blank=True, null=True, verbose_name="group")
    institution = models.CharField(max_length=100, blank=True, null=True, verbose_name="institution")
    skills = models.ManyToManyField(Skill, blank=True, related_name="profile_skill", verbose_name="skills")

    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.group})"
