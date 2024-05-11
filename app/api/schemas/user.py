from pydantic import BaseModel, Field, EmailStr


class UserBase(BaseModel):
    username: str = Field(..., example="johndoe", min_length=3, max_length=50)
    email: EmailStr = Field(..., example="johndoe@example.com")


class UserRegister(UserBase):
    password: str = Field(..., example="securepassword", min_length=6)
    role: int = Field(..., example=1)


class UserDisplay(UserBase):
    id: str = Field(..., example="1234567890abcdef")
    role: int = Field(..., example=1)
