from django.db import IntegrityError

from app.db.models.issued_token import IssuedToken
from app.db.models.platform_user import PlatformUser
from app.domain.interfaces.auth_interface import IAuthRepository


class AuthRepository(IAuthRepository):
    def create_token(self, jti: str, user: PlatformUser, device_id: str) -> bool:
        try:
            IssuedToken.objects.create(jti=jti, user=user, device_id=device_id)
        except IntegrityError:
            return None

        return True

    def revoke_token(self, jti: str, device_id: str) -> bool:
        revoked = IssuedToken.objects.filter(jti=jti, device_id=device_id, revoked=False).update(revoked=True)
        return revoked > 0

    def get_active_token(self, jti: str) -> IssuedToken:
        return IssuedToken.objects.filter(jti=jti, revoked=False).first()

    def revoke_all_user_tokens(self, user_id: int, device_id: str) -> bool:
        revoked = IssuedToken.objects.filter(user__user_id=user_id, device_id=device_id, revoked=False).update(
            revoked=True
        )
        return revoked > 0
