from typing import List
from uuid import UUID

from app.db.repositories.assignment_repository import AssignmentRepository
from app.domain.entities.assigment_schema import AssignmentOut, AssignmentSchema


class AssignmentService:
    def __init__(self, assignment_repo: AssignmentRepository):
        self._assignment_repo = assignment_repo

    def get_all_assignments(self) -> List[AssignmentOut]:
        return self._assignment_repo.get_all_assignments()

    def get_assignments_by_user(self, user_id: UUID) -> List[AssignmentOut]:
        return self._assignment_repo.get_assignments_by_user(user_id)

    def create_assignment(self, user_id: UUID, pool_id: int) -> AssignmentOut:
        return self._assignment_repo.create_assignment(user_id, pool_id)

    def update_assignment(self, user_id: UUID, assignment_id: int, annotation_data: AssignmentSchema) -> AssignmentOut:
        return self._assignment_repo.update_assignment(user_id, assignment_id, annotation_data)

    def update_assignment_status(self, user_id: UUID, assignment_id: int, status: str) -> AssignmentOut:
        return self._assignment_repo.update_assignment_status(user_id, assignment_id, status)
