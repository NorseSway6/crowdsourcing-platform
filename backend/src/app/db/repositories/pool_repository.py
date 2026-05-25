from typing import List
from uuid import UUID

from django.db import transaction
from ninja.errors import HttpError
from psycopg2 import IntegrityError

from app.db.models.pool import Pool
from app.db.models.skill import Skill
from app.db.models.task import Task
from app.domain.entities.pool_schema import PoolOut, PoolSchema
from app.domain.interfaces.pool_interface import IPoolRepository


class PoolRepository(IPoolRepository):
    def get_all_pools(self) -> List[PoolOut]:
        pools = Pool.objects.all()
        if not pools:
            raise HttpError(404, "Pools not found")
        return [PoolOut.from_orm(p) for p in pools]

    def get_pool_by_id(self, pool_id: int) -> PoolOut:
        pool = Pool.objects.filter(pool_id=pool_id).first()
        if pool is None:
            raise HttpError(404, "Pool not found")
        return pool

    def get_next_pool_by_order(self, pipeline_id: int, current_order: int):
        return Pool.objects.filter(pipeline_id=pipeline_id, order=current_order + 1).first()

    def create_pool(self, pipeline, index, pool_data: PoolSchema) -> Pool:
        return Pool.objects.create(
            pipeline=pipeline,
            order=index,
            points=pool_data.points,
            overlap=pool_data.overlap,
            pool_type=pool_data.pool_type,
        )

    def update_pool(self, pool_id: int, pool_data: PoolSchema) -> PoolOut:
        try:
            with transaction.atomic():
                pool = Pool.objects.filter(pool_id=pool_id).first()
                if not pool:
                    raise HttpError(404, "Pool not found")

                if pool_data.skills:
                    skill_names = list(set(pool_data.skills))
                    existing_skills = Skill.objects.filter(name__in=skill_names)

                    if existing_skills.count() != len(skill_names):
                        raise HttpError(404, "Some skills not found")

                    pool.skills.set(existing_skills)

                update_data = pool_data.dict(exclude={"skills"}, exclude_unset=True)
                for key, value in update_data.items():
                    setattr(pool, key, value)

                pool.save()
                return PoolOut.from_orm(pool)

        except IntegrityError:
            raise HttpError(409, "Update failed due to integrity error")
