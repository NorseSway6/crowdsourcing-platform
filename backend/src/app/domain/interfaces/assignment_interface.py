from typing import List
from uuid import UUID

from app.db.models.assignments import Assignment
from app.domain.entities.assigment_schema import AssignmentSchema


class IAssignmentRepository:
    def get_all_assignments(self) -> List[Assignment]:
        pass

    def get_assignments_by_user(self, user_id: UUID) -> List[Assignment]:
        pass

    def create_assignment(self, user_id: UUID) -> Assignment:
        pass

    def update_assignment(self, user_id: UUID, assignment_id: int, annotation_data: AssignmentSchema) -> Assignment:
        pass

    def update_assignment_status(self, user_id: UUID, assignment_id: int, status: str) -> Assignment:
        pass

    def get_assignment_by_id(self, user_id: UUID, assignment_id: int) -> Assignment:
        pass

    def get_active_assignment(self, user_id: UUID) -> Assignment:
        pass
