from django.db import models

from app.db.models.dataset import Dataset
from app.db.models.platform_user import PlatformUser


class Pipeline(models.Model):
    pipeline_id = models.BigAutoField(primary_key=True, verbose_name="pipline_id")
    dataset = models.ForeignKey(
        Dataset,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="pipline_dataset",
        verbose_name="dataset",
    )
    name = models.CharField(max_length=255, verbose_name="name")
    limit = models.IntegerField(null=True, blank=True, verbose_name="limit")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="created_at")
    owner = models.ForeignKey(PlatformUser, on_delete=models.CASCADE, related_name="pipline_user", verbose_name="user")

    def __str__(self):
        return f"{self.pipeline_id}"
