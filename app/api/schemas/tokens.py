from pydantic import BaseModel, Field, EmailStr


class Token(BaseModel):
    access_token: str
    token_type: str
    expires_in: int
    refresh_token: str
    