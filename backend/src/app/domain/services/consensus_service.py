from app.db.models.assignments import Assignment
from app.db.models.pool import Pool
from app.domain.entities.consensus_schema import ConsensusSchema
from app.domain.interfaces.assignment_interface import IAssignmentRepository
from app.domain.interfaces.pool_interface import IPoolRepository
from app.domain.interfaces.task_interface import ITaskRepository
from config import settings


class ConsensusService:
    def __init__(self, assignment_repo: IAssignmentRepository, pool_repo: IPoolRepository, task_repo: ITaskRepository):
        self._assignment_repo = assignment_repo
        self._pool_repo = pool_repo
        self._task_repo = task_repo

    def calculate_pool_consensus(self, task_id: int, current_pool_id: int) -> ConsensusSchema:
        annotations = self._assignment_repo._get_completed_annotations(task_id, current_pool_id)
        pool = self._pool_repo.get_pool_by_id(current_pool_id)
        total_votes = len(annotations)

        if total_votes < pool.overlap or not annotations:
            return ConsensusSchema(is_consensus_reached=False)

        if pool.pool_type == Pool.PoolType.ANNOTATION:
            return ConsensusSchema(is_consensus_reached=True, verdict="PENDING", final_annotation=annotations[0])

        elif pool.pool_type == Pool.PoolType.VERIFICATION:
            task = self._task_repo.get_task_by_id(task_id)
            target_annotation = task.annotation if hasattr(task, "annotation") else task.data.get("target_bbox")
            return self._calculate_verification_consensus(annotations, total_votes, target_annotation, pool.overlap)

        return ConsensusSchema(is_consensus_reached=False)

    def _resolve_assignments(
        self, task_id: int, current_pool_id: int, consensus_result: ConsensusSchema
    ) -> list[Assignment]:
        all_assignments = self._assignment_repo.get_ready_to_resolve_assignments(task_id, current_pool_id)
        pool = self._pool_repo.get_pool_by_id(current_pool_id)

        updated_assignments = []
        for assignment in all_assignments:
            if pool.pool_type == Pool.PoolType.ANNOTATION:
                assignment.status = Assignment.Status.PENDING
            elif pool.pool_type == Pool.PoolType.VERIFICATION:
                is_positive_vote = assignment.annotation.get("is_correct", False)
                is_consensus_approved = consensus_result.verdict == "APPROVED"
                is_good_work = is_consensus_approved == is_positive_vote
                assignment.status = Assignment.Status.APPROVED if is_good_work else Assignment.Status.REJECTED

            updated_assignments.append(assignment)

        return updated_assignments

    def _calculate_verification_consensus(
        self, annotation: list, total_votes: int, target_annotation: list, overlap: int
    ) -> ConsensusSchema:
        if not annotation:
            return ConsensusSchema(is_consensus_reached=False)

        positive_votes = 0
        for ann in annotation:
            vote = ann.get("is_correct") if isinstance(ann, dict) else ann
            if vote in [True, "true", "approved", "yes"]:
                positive_votes += 1

        approval_confidence = positive_votes / total_votes
        rejection_confidence = (total_votes - positive_votes) / total_votes

        if approval_confidence >= settings.VALIDATION_THRESHOLD:
            return ConsensusSchema(is_consensus_reached=True, verdict="APPROVED", final_annotation=target_annotation)
        elif rejection_confidence >= settings.VALIDATION_THRESHOLD:
            return ConsensusSchema(is_consensus_reached=True, verdict="REJECTED", final_annotation=target_annotation)

        if total_votes < overlap:
            return ConsensusSchema(is_consensus_reached=False)

        return ConsensusSchema(is_consensus_reached=True, verdict="REJECTED", final_annotation=target_annotation)
