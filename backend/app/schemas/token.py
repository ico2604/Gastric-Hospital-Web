from pydantic import BaseModel

class Token(BaseModel):
    access_token: str
    token_type: str
    user: dict # 또는 더 구체적인 UserSchema

class TokenData(BaseModel):
    email: str | None = None
