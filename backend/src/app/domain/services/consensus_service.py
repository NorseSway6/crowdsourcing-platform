import json
from collections import Counter
from typing import Union

from app.db.models.assignments import Assignment
from app.db.models.pool import Pool
from app.domain.entities.consensus_schema import ConsensusSchema
from app.domain.interfaces.assignment_interface import IAssignmentRepository
from app.domain.interfaces.pool_interface import IPoolRepository
from app.domain.interfaces.task_interface import ITaskRepository


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
            return self._majority_voiting(annotations, total_votes)

        elif pool.pool_type == Pool.PoolType.VERIFICATION:
            task = self._task_repo.get_task_by_id(task_id)
            target_annotation = task.annotation if hasattr(task, "annotation") else task.data.get("target_bbox")
            return self._calculate_verification_consensus(annotations, total_votes, target_annotation)

        elif pool.pool_type == Pool.PoolType.CLASSIFICATION:
            return self._calculate_classification_consensus(annotations, total_votes)

        return ConsensusSchema(is_consensus_reached=False)

    def _resolve_assignments(self, task_id: int, current_pool_id: int, consensus_result: ConsensusSchema) -> None:
        all_assignments = self._assignment_repo._get_all_for_task(task_id, current_pool_id)
        pool = self._pool_repo.get_pool_by_id(current_pool_id)

        assignments_to_update = []

        for assignment in all_assignments:
            is_good_work = False

            if pool.pool_type == Pool.PoolType.ANNOTATION:
                is_good_work = self._are_annotations_similar(assignment.annotation, consensus_result.final_annotation)

            elif pool.pool_type == Pool.PoolType.VERIFICATION:
                is_positive_vote = False
                if isinstance(assignment.annotation, dict):
                    is_positive_vote = assignment.annotation.get("is_correct") is True

                is_consensus_approved = consensus_result.verdict == "APPROVED"

                is_good_work = is_consensus_approved == is_positive_vote

            assignment.status = Assignment.Status.APPROVED if is_good_work else Assignment.Status.REJECTED
            assignments_to_update.append(assignment)

        updated = self._assignment_repo._bulk_update_assignments(assignments_to_update)
        if not updated:
            return None

    # ===== Consensus for aanotations =====
    def _majority_voiting(self, annotations: list, total_votes: int) -> ConsensusSchema:
        for i, target_ann in enumerate(annotations):
            agreement_count = 1

            for j, other_ann in enumerate(annotations):
                if i == j:
                    continue

                if self._are_annotations_similar(target_ann, other_ann):
                    agreement_count += 1

            confidence = agreement_count / total_votes

            if confidence > 0.5:
                return ConsensusSchema(is_consensus_reached=True, final_annotation=target_ann)

        return ConsensusSchema(is_consensus_reached=False)

    def _calculate_iou(self, bbox1: list, bbox2: list) -> float:
        if not bbox1 or not bbox2 or len(bbox1) != 4 or len(bbox2) != 4:
            return 0.0

        x1_min, y1_min, w1, h1 = bbox1
        x2_min, y2_min, w2, h2 = bbox2

        x1_max = x1_min + w1
        y1_max = y1_min + h1
        x2_max = x2_min + w2
        y2_max = y2_min + h2

        inter_x_min = max(x1_min, x2_min)
        inter_y_min = max(y1_min, y2_min)
        inter_x_max = min(x1_max, x2_max)
        inter_y_max = min(y1_max, y2_max)

        if inter_x_max <= inter_x_min or inter_y_max <= inter_y_min:
            return 0.0

        inter_area = (inter_x_max - inter_x_min) * (inter_y_max - inter_y_min)
        area1 = w1 * h1
        area2 = w2 * h2
        union_area = area1 + area2 - inter_area

        return inter_area / union_area if union_area > 0 else 0.0

    def _are_annotations_similar(
        self, ann1: Union[list, dict], ann2: Union[list, dict], iou_threshold: float = 0.75
    ) -> bool:
        data1 = ann1.get("items", ann1) if isinstance(ann1, dict) else ann1
        data2 = ann2.get("items", ann2) if isinstance(ann2, dict) else ann2

        if not isinstance(data1, list) or not isinstance(data2, list):
            return False

        for item1, item2 in zip(data1, data2):
            if not isinstance(item1, dict) or not isinstance(item2, dict):
                continue

            if item1.get("category_id") != item2.get("category_id"):
                return False

            iou = self._calculate_iou(item1.get("bbox", []), item2.get("bbox", []))
            if iou < iou_threshold:
                return False

        return True

    # ===== Consensus for verification =====
    def _calculate_verification_consensus(
        self, annotation: list, total_votes: int, target_annotation: list
    ) -> ConsensusSchema:
        if not annotation:
            return ConsensusSchema(is_consensus_reached=False)

        positive_votes = 0
        for ann in annotation:
            vote = ann.get("vote") if isinstance(ann, dict) else ann
            if vote in [True, "true", "approved", "yes"]:
                positive_votes += 1

        approval_confidence = positive_votes / total_votes
        rejection_confidence = (total_votes - positive_votes) / total_votes

        if approval_confidence >= 0.8:
            return ConsensusSchema(is_consensus_reached=True, verdict="APPROVED", final_annotation=target_annotation)
        elif rejection_confidence >= 0.8:
            return ConsensusSchema(is_consensus_reached=True, verdict="REJECTED", final_annotation=target_annotation)

        return ConsensusSchema(is_consensus_reached=False)
