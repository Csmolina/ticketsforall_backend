from typing import List
from pydantic import BaseModel


class UserBase(BaseModel):
    id: str
    name: str
    email: str
    user_type: str


class ListUsersResponseDto(BaseModel):
    users: List[UserBase]


class CreateUserRequestDto(BaseModel):
    id: str
    name: str
    email: str
    user_type: str


class CreateUserResponseDto(BaseModel):
    user: UserBase
