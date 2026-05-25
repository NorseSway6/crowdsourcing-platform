import os
import uuid

from django.db import models
from django.utils.translation import gettext_lazy as _

from app.db.models.dataset import Dataset
from app.db.models.pool import Pool


def get_task_upload_path(instance, filename):
    ext = filename.split(".")[-1]
    filename = f"{uuid.uuid4()}.{ext}"
    return os.path.join(f"dataset_{instance.dataset_id}", filename)


class Task(models.Model):
    class Status(models.TextChoices):
        AVAILABLE = "AVAILABLE", _("Available")
        COMPLETED = "COMPLETED", _("Completed")

    task_id = models.BigAutoField(primary_key=True, verbose_name="task_id")
    pool = models.ForeignKey(
        Pool, on_delete=models.SET_NULL, null=True, blank=True, related_name="task_pool", verbose_name="pool"
    )
    dataset = models.ForeignKey(Dataset, on_delete=models.CASCADE, related_name="task_dataset", verbose_name="dataset")
    image = models.ImageField(upload_to=get_task_upload_path)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="created_at")
    annotation = models.JSONField(default=list, null=True, blank=True, verbose_name="annotation")
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.AVAILABLE, verbose_name="status")

    @property
    def image_url(self) -> str:
        try:
            return self.image.url
        except (ValueError, AttributeError):
            return ""

    def __str__(self):
        return f"{self.task_id}"
