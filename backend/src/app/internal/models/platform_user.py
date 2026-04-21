from django.db import models
from django.utils.translation import gettext_lazy as _


class PlatformUser(models.Model):
    class Role(models.TextChoices):
        STUDENT = "STUDENT", _("Student")
        ADMIN = "ADMIN", _("Admin")

    user_id = models.BigIntegerField(primary_key=True, verbose_name="user_id")
    email = models.EmailField(unique=True, verbose_name="email")
    role = models.CharField(max_length=10, choices=Role.choices, default=Role.STUDENT, verbose_name="role")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="time")
    is_active = models.BooleanField(default=True, verbose_name="is_active")

    def __str__(self):
        return {self.user_id}
