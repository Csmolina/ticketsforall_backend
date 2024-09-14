from typing import NamedTuple

from core.src.models.user import User


class CreateUserResponse(NamedTuple):
    user: User
