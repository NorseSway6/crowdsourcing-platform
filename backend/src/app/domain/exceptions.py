from http import HTTPStatus


class DomainException(Exception):
    message: str = "A domain error occurred"
    error_code: str = "domain_error"
    status_code: int = HTTPStatus.BAD_REQUEST

    def __init__(self, message: str = None):
        if message:
            self.message = message
        super().__init__(self.message)


class EmptyDatasetError(DomainException):
    message = "Unassigned tasks not found for the specified dataset"
    error_code = "empty_dataset"
    status_code = HTTPStatus.NOT_FOUND


# ===== Pool exeptions =====
class PoolCompletionError(DomainException):
    message = "Failed to mark pool as completed"
    error_code = "pool_completion_failed"
    status_code = HTTPStatus.BAD_REQUEST


class PoolCreationFailedError(DomainException):
    error_code = "pool_creation_failed"
    status_code = HTTPStatus.BAD_REQUEST

    def __init__(self, step_index: int):
        super().__init__(f"Failed to create pool for pipeline step {step_index}")


class PoolNotFoundError(DomainException):
    message = "Pool not found"
    error_code = "pool_not_found"
    status_code = HTTPStatus.NOT_FOUND


class PoolMarkingError(DomainException):
    message = "Failed to mark pool"
    error_code = "pool_marking_failed"
    status_code = HTTPStatus.BAD_REQUEST


# ===== Pipeline exeptions =====
class PipelineCreationFailedError(DomainException):
    message = "Failed to create pipeline configuration"
    error_code = "pipeline_creation_failed"
    status_code = HTTPStatus.BAD_REQUEST


# ===== Task exeptions =====
class TaskMoveError(DomainException):
    message = "Failed to move task to the next pool"
    error_code = "task_move_failed"
    status_code = HTTPStatus.BAD_REQUEST


class TaskMarkingError(DomainException):
    message = "Failed to mark task"
    error_code = "task_marking_failed"
    status_code = HTTPStatus.BAD_REQUEST


class TaskLinkingFailedError(DomainException):
    message = "Failed to link tasks to the initial pool"
    error_code = "task_linking_failed"
    status_code = HTTPStatus.BAD_REQUEST


class TaskOperationError(DomainException):
    message = "Failed to perform operation on task"
    error_code = "task_op_failed"
    status_code = HTTPStatus.BAD_REQUEST


class TaskNotFoundError(DomainException):
    message = "Task not found"
    error_code = "task_not_found"
    status_code = HTTPStatus.NOT_FOUND


# ===== Assignment exeptions =====
class AssignmentOperationError(DomainException):
    message = "Failed to perform operation on assignment"
    error_code = "assignment_op_failed"
    status_code = HTTPStatus.BAD_REQUEST


class AssignmentNotFoundError(DomainException):
    message = "Assignment not found"
    error_code = "assignment_not_found"
    status_code = HTTPStatus.NOT_FOUND


class AssignmentCreationError(DomainException):
    message = "Failed to create assignment"
    error_code = "assignment_creation_failed"
    status_code = HTTPStatus.BAD_REQUEST


class AssignmentUpdatingError(DomainException):
    message = "Failed to update assignment"
    error_code = "assignment_updating_failed"
    status_code = HTTPStatus.BAD_REQUEST


# ===== Consensus exeptions =====
class ConsensusResolutionError(DomainException):
    message = "Failed to resolve consensus for task"
    error_code = "consensus_resolution_failed"
    status_code = HTTPStatus.BAD_REQUEST
