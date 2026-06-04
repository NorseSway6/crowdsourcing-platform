from ninja import Schema


class LogIn(Schema):
    email: str


class RefreshTokenIn(Schema):
    refresh_token: str


class TokenOut(Schema):
    access_token: str
    refresh_token: str
    token_type: str = "Bearer"
