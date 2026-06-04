import uuid
from datetime import datetime, timezone
from enum import Enum

import jwt

from app.domain.entities.auth_schema import LogIn, RefreshTokenIn, TokenOut
from app.domain.interfaces.auth_interface import IAuthRepository
from app.domain.interfaces.platform_user_interface import IUserRepository
from config import settings


class TokenType(Enum):
    ACCESS = "access"
    REFRESH = "refresh"


class AuthService:
    def __init__(self, auth_repo: IAuthRepository, user_repo: IUserRepository):
        self._auth_repo = auth_repo
        self._user_repo = user_repo

    def create_tokens(self, data: LogIn) -> TokenOut:
        user = self._user_repo.get_user_by_email(data.email)
        if not user:
            return None

        jti = str(uuid.uuid4())
        device_id = str(uuid.uuid4())
        access_token = self._generate_token(
            TokenType.ACCESS, user.user_id, jti, device_id, user.role, settings.JWT_ACCESS_TOKEN_LIFETIME
        )
        refresh_token = self._generate_token(
            TokenType.REFRESH, user.user_id, jti, device_id, user.role, settings.JWT_REFRESH_TOKEN_LIFETIME
        )

        created = self._auth_repo.create_token(jti, user, device_id)
        if not created:
            return None

        return TokenOut(access_token=access_token, refresh_token=refresh_token, token_type="Bearer")

    def update_revoked_status(self, data: RefreshTokenIn) -> bool:
        try:
            payload = jwt.decode(data.refresh_token, settings.JWT_SECRET_KEY, algorithms=["HS256"])
        except jwt.InvalidTokenError:
            return None

        jti = payload.get("jti")
        device_id = payload.get("device_id")
        if not jti or not device_id:
            return None

        revoked = self._auth_repo.revoke_token(jti, device_id)
        if not revoked:
            return None

        return revoked

    def update_token(self, data: RefreshTokenIn) -> TokenOut:
        try:
            payload = jwt.decode(data.refresh_token, settings.JWT_SECRET_KEY, algorithms=["HS256"])
        except jwt.InvalidTokenError:
            return None

        jti = payload.get("jti")
        device_id = payload.get("device_id")
        if not jti or not device_id:
            return None

        issued = self._auth_repo.get_active_token(jti)
        if not issued:
            user_id = payload.get("user_id")
            if user_id and device_id:
                self._auth_repo.revoke_all_user_tokens(user_id, device_id)
            return None

        revoked = self._auth_repo.revoke_token(jti, device_id)
        if not revoked:
            return None

        new_jti = str(uuid.uuid4())
        new_device_id = str(uuid.uuid4())
        user = issued.user
        new_access = self._generate_token(
            TokenType.ACCESS, user.user_id, new_jti, new_device_id, user.role, settings.JWT_ACCESS_TOKEN_LIFETIME
        )
        new_refresh = self._generate_token(
            TokenType.REFRESH, user.user_id, new_jti, new_device_id, user.role, settings.JWT_REFRESH_TOKEN_LIFETIME
        )

        created = self._auth_repo.create_token(new_jti, user, new_device_id)
        if not created:
            return None

        return TokenOut(access_token=new_access, refresh_token=new_refresh, token_type="Bearer")

    def _generate_token(self, token_type, user_id, jti, device_id, role, lifetime):
        now = datetime.now(timezone.utc)
        exp = now + lifetime
        payload = {
            "user_id": str(user_id),
            "exp": exp,
            "type": token_type.value,
            "jti": jti,
            "device_id": device_id,
            "role": role,
        }

        return jwt.encode(payload, settings.JWT_SECRET_KEY, algorithm="HS256")
