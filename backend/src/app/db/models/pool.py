from django.db import models

from app.db.models.skill import Skill


class Pool(models.Model):
    pool_id = models.BigIntegerField(primary_key=True, verbose_name="pool_id")
    points = models.IntegerField(default=0, verbose_name="points")
    skills = models.ManyToManyField(Skill, related_name="pool_skill", verbose_name="skills")
    overlap = models.IntegerField(default=1, verbose_name="overlap")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="created_at")
    is_active = models.BooleanField(default=True, verbose_name="is_active")

    def __str__(self):
        return {self.pool_id}
