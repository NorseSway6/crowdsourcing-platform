import app.domain.exceptions as exc
from app.db.models.platform_user import PlatformUser


class IsStudent:
    def check(self, request, user) -> None:
        if user.role != PlatformUser.Role.STUDENT:
            raise exc.AuthAccessError()


class IsCustomer:
    def check(self, request, user) -> None:
        if user.role != PlatformUser.Role.CUSTOMER:
            raise exc.AuthAccessError()


class AllowAll:
    def check(self, request, user) -> None:
        pass
