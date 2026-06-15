from django.db import transaction

import app.domain.exceptions as exc
from app.db.models.pool import Pool
from app.domain.entities.pool_schema import (
    PoolDetailOut,
    PoolFilter,
    PoolInstructionOut,
    PoolInstructionSchema,
    PoolOut,
    PoolSchema,
    PoolType,
)
from app.domain.interfaces.pool_interface import IPoolRepository
from app.domain.interfaces.skill_interface import ISkillRepository
from app.domain.interfaces.task_interface import ITaskRepository
from config import settings


class PoolService:
    def __init__(self, pool_repo: IPoolRepository, skill_repo: ISkillRepository, task_repo: ITaskRepository):
        self._pool_repo = pool_repo
        self._skill_repo = skill_repo
        self._task_repo = task_repo

    def get_all_pools(self, filters: PoolFilter) -> list[PoolOut]:
        pools = self._pool_repo.get_all_pools(filters)
        if not pools:
            raise exc.PoolNotFoundError()
        return [PoolOut.from_orm(pool) for pool in pools]

    def get_pool_by_id(self, pool_id: int) -> PoolOut:
        pool = self._pool_repo.get_pool_by_id(pool_id)
        if not pool:
            raise exc.PoolNotFoundError()
        return PoolOut.from_orm(pool)

    def update_pool(self, pool_id: int, pool_data: PoolSchema) -> PoolOut:
        with transaction.atomic():
            pool = self._pool_repo.get_pool_by_id(pool_id)
            if not pool:
                raise exc.PoolNotFoundError()

            if pool_data.skills:
                skill_names = list(set(pool_data.skills))
                existing_skills = self._skill_repo.get_skills_by_names(skill_names)

                if len(existing_skills) != len(skill_names):
                    raise exc.SkillNotFoundError()

                pool.skills.set(existing_skills)

            update_fields = pool_data.dict(exclude={"skills"}, exclude_unset=True)
            for attr, value in update_fields.items():
                setattr(pool, attr, value)

            updated = self._pool_repo.update_pool(pool)
            if not updated:
                raise exc.PoolUpdatingError()

            return PoolOut.from_orm(pool)

    def create_pool(self, pipeline, index, pool_data: PoolSchema) -> PoolOut:
        if pool_data.pool_type == PoolType.ANNOTATION:
            overlap = settings.OVERLAP_ANNOTATION
        elif pool_data.pool_type == PoolType.VERIFICATION:
            overlap = settings.OVERLAP_VERIFICATION

        with transaction.atomic():
            pool = self._pool_repo.create_pool(pipeline, index, pool_data, overlap)
            if not pool:
                raise exc.PoolCreationFailedError(index)

            if pool_data.skills:
                skill_names = list(set(pool_data.skills))
                existing_skills = self._skill_repo.get_skills_by_names(skill_names)

                if len(existing_skills) != len(skill_names):
                    raise exc.SkillNotFoundError()

                pool.skills.add(*existing_skills)

            return PoolOut.from_orm(pool)

    def try_complete_pool(self, pool: Pool) -> bool:
        unfinished_tasks_count = self._task_repo.count_unfinished_tasks(pool.pool_id)

        if unfinished_tasks_count == 0:
            marked = self._pool_repo._mark_pool_completed(pool.pool_id)
            if not marked:
                raise exc.PoolMarkingError()
            return True

        return False

    def _get_next_pool_in_pipeline(self, current_pool_id: int) -> int:
        current_pool = self._pool_repo.get_pool_by_id(current_pool_id)
        if not current_pool:
            raise exc.PoolNotFoundError()

        next_pool = self._pool_repo.get_next_pool_by_order(
            pipeline_id=current_pool.pipeline_id, current_order=current_pool.order
        )
        if not next_pool:
            raise exc.PoolNotFoundError()

        return next_pool.pool_id

    def create_instruction(self, pool_id: int, instruction: PoolInstructionSchema) -> PoolDetailOut:
        with transaction.atomic():
            new_instruction = self._pool_repo.create_instruction(instruction.content_markdown, instruction.title)
            if not new_instruction:
                raise exc.InstructionCreationFailedError()

            pool = self._pool_repo.get_pool_by_id(pool_id)
            if not pool:
                raise exc.PoolNotFoundError()

            updated_pool = self._pool_repo.update_pool_instruction(pool, new_instruction.id)
            if not updated_pool:
                raise exc.PoolUpdatingError()

            return PoolDetailOut.from_orm(updated_pool)

    def get_instruction_by_id(self, instruction_id: int) -> PoolInstructionOut:
        instruction = self._pool_repo.get_instruction_by_id(instruction_id)
        if not instruction:
            raise exc.InstructionNotFoundError()
        return PoolInstructionOut.from_orm(instruction)

    def get_instruction_by_pool(self, pool_id: int) -> PoolInstructionOut:
        instruction = self._pool_repo.get_instruction_by_pool(pool_id)
        if not instruction:
            raise exc.InstructionNotFoundError()
        return PoolInstructionOut.from_orm(instruction)
