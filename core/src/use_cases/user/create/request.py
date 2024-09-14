from typing import NamedTuple
from pydantic import EmailStr


class CreateUserRequest(NamedTuple):
    name: str
    email: EmailStr
