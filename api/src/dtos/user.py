from typing import List
from pydantic import BaseModel, EmailStr


class UserBase(BaseModel):
    id: int
    name: str
    email: EmailStr
    user_type: str


class ListUsersResponseDto(BaseModel):
    users: List[UserBase]


class CreateUserRequestDto(BaseModel):
    name: str
    email: EmailStr


class CreateUserResponseDto(BaseModel):
    user: UserBase
