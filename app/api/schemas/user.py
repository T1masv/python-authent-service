from pydantic import BaseModel, Field, EmailStr
from enum import Enum


class Roles(Enum):
    ADMIN = 2
    PROPRIO = 1
    LOCATAIRE = 0


class UserBase(BaseModel):
    username: str = Field(..., example="johndoe", min_length=3, max_length=50)


class LoginUser(UserBase):
    password: str = Field(..., exemple="password")


class RegisterUser(LoginUser):
    role: Roles = Field(..., exemple=1)
    email: EmailStr = Field(..., exemple="johndoe@example.com")


class DisplayUser(UserBase):
    role: Roles = Field(..., exemple=1)
    email: EmailStr = Field(..., example="johndoe@example.com")

