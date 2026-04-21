from django.db import models

from app.internal.models.platform_user import PlatformUser
from app.internal.models.task import Task


class AuditLog(models.Model):
    audit_id = models.BigIntegerField(primary_key=True, verbose_name="audit_id")
    user = models.ForeignKey(PlatformUser, on_delete=models.CASCADE, related_name="audit_user", verbose_name="user")
    task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name="audit_task", verbose_name="task")
    action = models.CharField(max_length=255, verbose_name="action")
    timestamp = models.DateTimeField(auto_now_add=True, verbose_name="timestamp")
    ip_address = models.GenericIPAddressField(verbose_name="ip_address")

    def __str__(self):
        return {self.audit_id}
