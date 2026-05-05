from typing import List
from uuid import UUID

from app.domain.entities.assigment_schema import AssignmentOut, AssignmentSchema


class IAssignmentRepository:
    def get_all_assignments(self) -> List[AssignmentOut]:
        pass

    def get_assignment_tasks(self, user_id: UUID) -> List[AssignmentOut]:
        pass

    def create_assignment(self, user_id: UUID, pool_id: int) -> AssignmentOut:
        pass

    def update_assignment(self, user_id: UUID, assignment_id: int, annotation_data: AssignmentSchema) -> AssignmentOut:
        pass

    def update_assignment_status(self, user_id: UUID, assignment_id: int, status: str) -> AssignmentOut:
        pass
