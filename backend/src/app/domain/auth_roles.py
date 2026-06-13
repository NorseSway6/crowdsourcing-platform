from enum import Enum
from functools import wraps
from http import HTTPStatus

from ninja.errors import HttpError

import app.domain.exceptions as exc
from app.db.models.platform_user import PlatformUser


class AuthRole(Enum):
    ADMIN = PlatformUser.Role.ADMIN
    CUSTOMER = PlatformUser.Role.CUSTOMER
    STUDENT = PlatformUser.Role.STUDENT


def has_roles(*roles: PlatformUser.Role):
    def decorator(func):
        @wraps(func)
        def wrapper(request, *args, **kwargs):
            user = getattr(request, "auth", None)

            allowed_role_values = [role.value for role in roles]

            if not user:
                raise exc.UnauthorizedError()

            if user.role not in allowed_role_values:
                raise exc.AccessError()

            return func(request, *args, **kwargs)

        return wrapper

    return decorator
