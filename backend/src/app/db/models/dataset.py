from django.db import models

from app.db.models.platform_user import PlatformUser


class Dataset(models.Model):
    dataset_id = models.BigIntegerField(primary_key=True, verbose_name="dataset_id")
    name = models.CharField(max_length=255, verbose_name="name")
    domain = models.CharField(max_length=255, verbose_name="domain")
    owner = models.ForeignKey(PlatformUser, on_delete=models.CASCADE, related_name="dataset_user", verbose_name="owner")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="created_at")

    def __str__(self):
        return f"{self.dataset_id}"
