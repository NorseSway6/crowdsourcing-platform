from django.db import IntegrityError

from app.db.models.pool import Pool, PoolInstruction
from app.domain.entities.pool_schema import PoolFilter, PoolSchema
from app.domain.interfaces.pool_interface import IPoolRepository


class PoolRepository(IPoolRepository):
    def get_all_pools(self, filters: PoolFilter) -> list[Pool]:
        queryset = Pool.objects.prefetch_related("skills")

        if filters.skills:
            queryset = queryset.filter(skills__name__in=filters.skills).distinct()

        if filters.max_points:
            queryset = queryset.filter(points__lte=filters.max_points)

        if filters.min_points:
            queryset = queryset.filter(points__gte=filters.min_points)

        if filters.institution:
            queryset = queryset.filter(target_institution=filters.institution)

        return list(queryset.all())

    def get_pool_by_id(self, pool_id: int) -> Pool:
        return Pool.objects.select_related("instruction").filter(pool_id=pool_id).first()

    def get_next_pool_by_order(self, pipeline_id: int, current_order: int) -> Pool:
        return Pool.objects.filter(pipeline_id=pipeline_id, order=current_order + 1).first()

    def create_pool(self, pipeline, index, pool_data: PoolSchema, overlap: int) -> Pool:
        try:
            pool = Pool.objects.create(
                pipeline=pipeline,
                order=index,
                points=pool_data.points,
                overlap=overlap,
                pool_type=pool_data.pool_type,
                target_institution=pool_data.target_institution,
                tasks_limit=pool_data.tasks_limit,
                instruction_id=pool_data.instruction_id,
            )
        except IntegrityError:
            return None

        return pool

    def update_pool(self, pool: Pool) -> Pool:
        try:
            pool.save()
        except IntegrityError:
            return None

        return pool

    def _mark_pool_completed(self, pool_id: int) -> bool:
        updated = Pool.objects.filter(pool_id=pool_id).update(status=Pool.PoolStatus.COMPLETED)
        return updated > 0

    def _get_pool_by_type(self, pipeline_id: int, pool_type: str) -> Pool:
        return Pool.objects.filter(pipeline_id=pipeline_id, pool_type=pool_type).first()

    def create_instruction(self, content: str, title: str) -> PoolInstruction:
        try:
            created = PoolInstruction.objects.create(content_markdown=content, title=title)
        except IntegrityError:
            return None

        return created

    def update_pool_instruction(self, pool: Pool, instruction_id: int) -> Pool:
        pool.instruction_id = instruction_id
        try:
            pool.save()
        except IntegrityError:
            return None

        return pool

    def get_instruction_by_id(self, instruction_id: int) -> PoolInstruction:
        return PoolInstruction.objects.filter(id=instruction_id).first()

    def get_instruction_by_pool(self, pool_id: int) -> PoolInstruction:
        return PoolInstruction.objects.filter(pool_instruction__pool_id=pool_id).first()
