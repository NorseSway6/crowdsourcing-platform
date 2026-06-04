from django.db import models

from app.db.models.platform_user import PlatformUser


class IssuedToken(models.Model):
    jti = models.CharField(max_length=255, primary_key=True)
    user = models.ForeignKey(PlatformUser, on_delete=models.CASCADE, related_name="refresh_tokens")
    created_at = models.DateTimeField(auto_now_add=True)
    revoked = models.BooleanField(default=False)
    device_id = models.UUIDField(unique=True)
