from uuid import UUID

from app.db.models.assignments import Assignment


class IAssignmentRepository:
    def get_assignments_by_user(self, user_id: UUID) -> list[Assignment]:
        pass

    def get_assignment_by_id(self, user_id: UUID, assignment_id: int) -> Assignment:
        pass

    def create_assignment(self, user_id: UUID, task_id: int) -> Assignment:
        pass

    def update_assignment(self, data: Assignment) -> Assignment:
        pass

    def _get_active_assignment(self, user_id: UUID) -> Assignment:
        pass

    def _get_completed_annotations(self, task_id: int, pool_id: int) -> list[dict]:
        pass

    def _get_all_for_task(self, task_id: int, current_pool_id: int) -> list[Assignment]:
        pass

    def _bulk_update_assignments(self, assignments: list[Assignment]) -> None:
        pass
