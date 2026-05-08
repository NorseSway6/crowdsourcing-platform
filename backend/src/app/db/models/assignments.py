from django.db import models
from django.utils.translation import gettext_lazy as _

from app.db.models.platform_user import PlatformUser
from app.db.models.task import Task


class Assignment(models.Model):
    class Status(models.TextChoices):
        IN_PROGRESS = "IN_PROGRESS", _("In Progress")
        PENDING = "PENDING", _("Pending")
        APPROVED = "APPROVED", _("Approved")
        REJECTED = "REJECTED", _("Rejected")

    assignment_id = models.BigAutoField(primary_key=True, verbose_name="assignment_id")
    task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name="assignment_task", verbose_name="task")
    user = models.ForeignKey(
        PlatformUser, on_delete=models.CASCADE, related_name="assignment_user", verbose_name="user"
    )
    annotation = models.JSONField(default=list, verbose_name="annotation")
    started_at = models.DateTimeField(auto_now_add=True, verbose_name="started_at")
    completed_at = models.DateTimeField(null=True, blank=True, verbose_name="completed_at")
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.IN_PROGRESS, verbose_name="status")

    def __str__(self):
        return f"{self.assignment_id}"
