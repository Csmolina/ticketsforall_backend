from typing import NamedTuple


class CreateUserRequest(NamedTuple):
    id: str
    name: str
    email: str
    user_type: str
