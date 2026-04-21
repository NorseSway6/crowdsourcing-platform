from django.db import models
from django.utils.translation import gettext_lazy as _

from app.internal.models.dataset import Dataset


class Task(models.Model):
    class Status(models.TextChoices):
        QUEUED = "QUEUED", _("In Queue")
        IN_PROGRESS = "IN_PROGRESS", _("In Progress")
        COMPLETED = "COMPLETED", _("Completed")
        ARCHIVED = "ARCHIVED", _("Archived")

    class Stage(models.TextChoices):
        ANNOTATION = "ANNOTATION", _("Annotation")
        VERIFICATION = "VERIFICATION", _("Verification")
        REVIEW = "REVIEW", _("Review")

    task_id = models.BigIntegerField(primary_key=True, verbose_name="task_id")
    dataset = models.ForeignKey(Dataset, on_delete=models.CASCADE, related_name="task_dataset", verbose_name="dataset")
    image = models.CharField(max_length=500)
    current_stage = models.CharField(
        max_length=20, choices=Stage.choices, default=Stage.ANNOTATION, verbose_name="current_stage"
    )
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.QUEUED, verbose_name="status")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="created_at")

    def __str__(self):
        return {self.task_id}
