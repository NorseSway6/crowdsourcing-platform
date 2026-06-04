import jwt
from django.conf import settings
from ninja.security import HttpBearer

from app.db.models.issued_token import IssuedToken
from app.db.models.platform_user import PlatformUser
from app.domain.auth_roles import IsAdmin, IsCustomer, IsStudent


class JWTAuth(HttpBearer):
    def __init__(self, permissions=None):
        self.permissions = permissions
        super().__init__()

    def authenticate(self, request, token: str):
        try:
            payload = jwt.decode(token, settings.JWT_SECRET_KEY, algorithms=["HS256"])

            user = PlatformUser.objects.get(user_id=payload["user_id"])

            for permission in self.permissions:
                permission.check(request, user)
        except jwt.InvalidTokenError:
            return None

        if payload.get("type") != "access":
            return None

        user_id = payload.get("user_id")
        if not user_id:
            return None

        role = payload.get("role")
        if not role:
            return None

        jti = payload.get("jti")
        if not jti:
            return None

        try:
            issued = IssuedToken.objects.select_related("user").get(jti=jti, revoked=False)
        except IssuedToken.DoesNotExist:
            return None

        return issued.user


student_auth = JWTAuth(permissions=[IsStudent()])
customer_auth = JWTAuth(permissions=[IsCustomer()])
admin_auth = JWTAuth(permissions=[IsAdmin()])
