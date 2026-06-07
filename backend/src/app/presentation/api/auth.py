import jwt
from django.conf import settings
from ninja.security import HttpBearer

from app.db.models.issued_token import IssuedToken


class JWTAuth(HttpBearer):
    def __init__(self, permissions=None):
        self.permissions = permissions
        super().__init__()

    def authenticate(self, request, token: str):
        try:
            payload = jwt.decode(token, settings.JWT_SECRET_KEY, algorithms=["HS256"])
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
