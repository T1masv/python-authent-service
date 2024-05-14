from bson import ObjectId
from pydantic import BaseModel, Field, EmailStr, field_validator, field_serializer
from enum import Enum
from typing import Any

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
    telephone: str = Field(..., example="1234567891", min_length=10, max_length=10)

    @field_serializer('role')
    def serialize_role(self, role):
        return role.value


class DisplayUser(UserBase):
    id: Any = Field(validation_alias="_id")
    role: Roles = Field(exemple=1)
    email: EmailStr = Field(example="johndoe@example.com")
    telephone: str = Field(example="1234567891", min_length=10, max_length=10)

    @field_serializer('id')
    def serialize_id(self, id):
        return str(id)

    @field_serializer('role')
    def serialize_role(self, role):
        return role.value
