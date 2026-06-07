from http import HTTPStatus


class DomainException(Exception):
    message: str = "A domain error occurred"
    error_code: str = "domain_error"
    status_code: int = HTTPStatus.BAD_REQUEST

    def __init__(self, message: str = None):
        if message:
            self.message = message
        super().__init__(self.message)


# ===== Dataset exeptions =====
class EmptyDatasetError(DomainException):
    message = "Unassigned tasks not found for the specified dataset"
    error_code = "empty_dataset"
    status_code = HTTPStatus.NOT_FOUND


class DatasetNotFoundError(DomainException):
    message = "Dataset not found"
    error_code = "dataset_not_found"
    status_code = HTTPStatus.NOT_FOUND


class DatasetCreationFailedError(DomainException):
    message = "Failed to create dataset"
    error_code = "dataset_creation_failed"
    status_code = HTTPStatus.BAD_REQUEST


class DatasetUpdatingError(DomainException):
    message = "Failed to update dataset"
    error_code = "dataset_updating_failed"
    status_code = HTTPStatus.BAD_REQUEST


class DatasetDeletionError(DomainException):
    message = "Dataset deletion error"
    error_code = "dataset_deletion_error"
    status_code = HTTPStatus.BAD_REQUEST


class UploadImageError(DomainException):
    message = "Upload image error"
    error_code = "image_upload_error"
    status_code = HTTPStatus.BAD_REQUEST


class CategoriesNotFoundError(DomainException):
    message = "Categories not found"
    error_code = "categories_not_found"
    status_code = HTTPStatus.NOT_FOUND


class CreateCategoryError(DomainException):
    message = "Create categories error"
    error_code = "categories_create_error"
    status_code = HTTPStatus.BAD_REQUEST


class DeleteCategorysError(DomainException):
    message = "Delete categories error"
    error_code = "categories_delete_error"
    status_code = HTTPStatus.BAD_REQUEST


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


class PoolUpdatingError(DomainException):
    message = "Failed to update pool"
    error_code = "pool_updating_failed"
    status_code = HTTPStatus.BAD_REQUEST


# ===== Pipeline exeptions =====
class PipelineCreationFailedError(DomainException):
    message = "Failed to create pipeline configuration"
    error_code = "pipeline_creation_failed"
    status_code = HTTPStatus.BAD_REQUEST


class PipelineNotFoundError(DomainException):
    message = "Pipeline not found"
    error_code = "pipeline_not_found"
    status_code = HTTPStatus.NOT_FOUND


class PipelineUpdatingError(DomainException):
    message = "Failed to update pipeline"
    error_code = "pipeline_updating_failed"
    status_code = HTTPStatus.BAD_REQUEST


class PipelineDeletionError(DomainException):
    message = "Pipeline deletion error"
    error_code = "pipeline_deletion_error"
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


class TaskDeletionError(DomainException):
    message = "Task deletion error"
    error_code = "task_deletion_error"
    status_code = HTTPStatus.BAD_REQUEST


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


# ===== Skill exeptions =====
class SkillNotFoundError(DomainException):
    message = "Skill not found"
    error_code = "skill_not_found"
    status_code = HTTPStatus.NOT_FOUND


class SkillCreationError(DomainException):
    message = "Failed to create skill"
    error_code = "skill_creation_failed"
    status_code = HTTPStatus.BAD_REQUEST


class SkillDeletionError(DomainException):
    message = "Skill deletion error"
    error_code = "skill_deletion_error"
    status_code = HTTPStatus.BAD_REQUEST


# ===== User exeptions =====
class UserCreationFailedError(DomainException):
    message = "Failed to create user"
    error_code = "user_creation_failed"
    status_code = HTTPStatus.BAD_REQUEST


class ProfileCreationFailedError(DomainException):
    message = "Profile to create user"
    error_code = "profile_creation_failed"
    status_code = HTTPStatus.BAD_REQUEST


class UserNotFoundError(DomainException):
    message = "User not found"
    error_code = "user_not_found"
    status_code = HTTPStatus.NOT_FOUND


class ProifleUpdatingError(DomainException):
    message = "Profile to update assignment"
    error_code = "profile_updating_failed"
    status_code = HTTPStatus.BAD_REQUEST


class UserDeletionError(DomainException):
    message = "User deletion error"
    error_code = "user_deletion_error"
    status_code = HTTPStatus.BAD_REQUEST


# ===== Consensus exeptions =====
class ConsensusResolutionError(DomainException):
    message = "Failed to resolve consensus for task"
    error_code = "consensus_resolution_failed"
    status_code = HTTPStatus.BAD_REQUEST


# ===== Auth exeptions =====
class AuthLoginError(DomainException):
    message = "Wrong password or email"
    error_code = "failed_login"
    status_code = HTTPStatus.BAD_REQUEST


class AuthCreateError(DomainException):
    message = "Create token error"
    error_code = "failed_create_roken"
    status_code = HTTPStatus.BAD_REQUEST


class AuthRevokeError(DomainException):
    message = "Revoke token error"
    error_code = "failed_revoke_token"
    status_code = HTTPStatus.BAD_REQUEST
