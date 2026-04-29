from django.db import models
from django.utils.translation import gettext_lazy as _

from app.db.models.dataset import Dataset
from app.db.models.pool import Pool


class Task(models.Model):
    task_id = models.BigIntegerField(primary_key=True, verbose_name="task_id")
    pool = models.ForeignKey(Pool, on_delete=models.CASCADE, related_name="task_pool", verbose_name="pool")
    dataset = models.ForeignKey(Dataset, on_delete=models.CASCADE, related_name="task_dataset", verbose_name="dataset")
    image_url = models.URLField()
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="created_at")

    def __str__(self):
        return f"{self.task_id}"
