from django.db import models

from app.db.models.pipeline import Pipeline
from app.db.models.skill import Skill


class PoolInstruction(models.Model):
    title = models.CharField(max_length=255)
    content_markdown = models.TextField()


class Pool(models.Model):
    class PoolType(models.TextChoices):
        ANNOTATION = "ANNOTATION", "Annotation"
        VERIFICATION = "VERIFICATION", "Verification"

    class PoolStatus(models.TextChoices):
        OPEN = "OPEN", "Open"
        COMPLETED = "COMPLETED", "Completed"

    pool_id = models.BigAutoField(primary_key=True, verbose_name="pool_id")
    pipeline = models.ForeignKey(
        Pipeline, on_delete=models.CASCADE, null=True, blank=True, related_name="pool_pipeline", verbose_name="pipline"
    )
    order = models.IntegerField(default=1, verbose_name="order")
    points = models.IntegerField(default=0, verbose_name="points")
    skills = models.ManyToManyField(Skill, related_name="pool_skill", verbose_name="skills")
    overlap = models.IntegerField(default=1, verbose_name="overlap")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="created_at")
    pool_type = models.CharField(max_length=50, choices=PoolType.choices, default=PoolType.ANNOTATION)
    status = models.CharField(max_length=50, choices=PoolStatus.choices, default=PoolStatus.OPEN)
    target_institution = models.CharField(max_length=100, blank=True, null=True, verbose_name="target_institution")
    tasks_limit = models.IntegerField(default=10, verbose_name="tasks_limit")
    time_limit = models.IntegerField(default=600, verbose_name="time_limit")
    instruction = models.ForeignKey(
        PoolInstruction, on_delete=models.SET_NULL, null=True, blank=True, related_name="pool_instruction"
    )

    @property
    def skill_names(self):
        return [s.name for s in self.skills.all()]

    def __str__(self):
        return f"{self.pool_id}"
