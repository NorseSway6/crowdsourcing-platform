from app.db.models.issued_token import IssuedToken
from app.db.models.platform_user import PlatformUser


class IAuthRepository:
    def create_token(self, jti: str, user: PlatformUser, device_id: str) -> bool:
        pass

    def revoke_token(self, jti: str, device_id: str) -> bool:
        pass

    def get_active_token(self, jti: str) -> IssuedToken:
        pass

    def revoke_all_user_tokens(self, user_id: int, device_id: str) -> bool:
        pass
