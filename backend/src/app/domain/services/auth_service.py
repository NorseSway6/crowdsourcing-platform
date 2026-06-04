import uuid
from datetime import datetime, timezone
from enum import Enum

import jwt
from django.contrib.auth.hashers import check_password, make_password

import app.domain.exceptions as exc
from app.domain.entities.auth_schema import LogIn, RefreshTokenIn, TokenOut
from app.domain.entities.platform_user_schema import RegisterOut, RegisterSchema, UserOut
from app.domain.interfaces.auth_interface import IAuthRepository
from app.domain.interfaces.platform_user_interface import IUserRepository
from app.domain.services.platform_user_service import UserService
from config import settings


class TokenType(Enum):
    ACCESS = "access"
    REFRESH = "refresh"


class AuthService:
    def __init__(self, auth_repo: IAuthRepository, user_repo: IUserRepository, user_service: UserService):
        self._auth_repo = auth_repo
        self._user_repo = user_repo
        self._user_service = user_service

    def create_tokens(self, data: LogIn) -> TokenOut:
        user = self._user_repo.get_user_by_email(data.email)
        if not user or not check_password(data.password, user.password):
            raise exc.AuthLoginError()

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
            return exc.AuthCreateError()

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
            raise exc.AuthRevokeError()

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
            raise exc.AuthRevokeError()

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
            raise exc.AuthCreateError()

        return TokenOut(access_token=new_access, refresh_token=new_refresh, token_type="Bearer")

    def register_user(self, data: RegisterSchema) -> RegisterOut:
        hashed_password = make_password(data.password)
        data.password = hashed_password

        new_user = self._user_service.create_user(data)
        user = self._user_repo.get_user_by_email(new_user.email)
        if not user:
            return exc.UserNotFoundError()

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
            return exc.AuthCreateError()

        return RegisterOut(
            user=UserOut.from_orm(user),
            tokens=TokenOut(access_token=access_token, refresh_token=refresh_token, token_type="Bearer"),
        )

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
