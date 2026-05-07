import uuid

from django.db import models
from django.utils.translation import gettext_lazy as _


class PlatformUser(models.Model):
    class Role(models.TextChoices):
        STUDENT = "STUDENT", _("Student")
        ADMIN = "ADMIN", _("Admin")
        VALIDATOR = "VALIDATOR", _("Validator")

    user_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email = models.EmailField(unique=True, verbose_name="email")
    role = models.CharField(max_length=10, choices=Role.choices, default=Role.STUDENT, verbose_name="role")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="time")
    is_active = models.BooleanField(default=True, verbose_name="is_active")

    def __str__(self):
        return f"{self.user_id}"
