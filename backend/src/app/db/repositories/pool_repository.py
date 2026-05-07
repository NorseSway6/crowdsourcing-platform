from typing import List
from uuid import UUID

from django.db import transaction
from ninja.errors import HttpError
from psycopg2 import IntegrityError

from app.db.models.pool import Pool
from app.db.models.skill import Skill
from app.db.models.task import Task
from app.domain.entities.pool_schema import PoolOut, PoolSchema
from app.domain.entities.task_schema import TaskOut, TaskSchema
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
        return PoolOut.from_orm(pool)

    def create_pool(self, pool_data: PoolSchema) -> PoolOut:
        skill_names = list({s.name for s in pool_data.skills})

        try:
            with transaction.atomic():
                pool = Pool.objects.create(points=pool_data.points, overlap=pool_data.overlap)

                if pool_data.skills:
                    existing_skills = Skill.objects.filter(name__in=skill_names)

                    if len(existing_skills) != len(skill_names):
                        raise HttpError(404, "Some skills not found")

                    pool.skills.add(*existing_skills)
        except IntegrityError:
            raise HttpError(409, "Create failed due to integrity error")

        return PoolOut.from_orm(pool)

    def update_pool(self, pool_id: int, pool_data: PoolSchema) -> PoolOut:
        try:
            with transaction.atomic():
                pool = Pool.objects.filter(pool_id=pool_id).first()
                if not pool:
                    raise HttpError(404, "Pool not found")

                if pool_data.skills is not None:
                    skill_names = list({s.name for s in pool_data.skills})
                    existing_skills = Skill.objects.filter(name__in=skill_names)

                    if len(existing_skills) != len(skill_names):
                        raise HttpError(404, "Some skills not found")

                    pool.skills.set(existing_skills)

                update_data = pool_data.dict(exclude={"skills"}, exclude_unset=True)
                for key, value in update_data.items():
                    setattr(pool, key, value)

                pool.save()
                return PoolOut.from_orm(pool)

        except IntegrityError:
            raise HttpError(409, "Update failed due to integrity error")

    def create_task(self, pool_id: int, dataset_id: int, task_data: TaskSchema) -> TaskOut:
        try:
            task = Task.objects.create(pool_id=pool_id, dataset_id=dataset_id, **task_data)
        except:
            raise HttpError(409, "Create failed due to integrity error")
        return TaskOut.from_orm(task)

    def delete_pool(self, pool_id: int) -> bool:
        deleted, _ = Pool.objects.filter(pool_id=pool_id).delete()
        if not deleted:
            raise HttpError(404, "Pool for delete not found")
        return deleted
