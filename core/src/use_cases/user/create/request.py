from typing import NamedTuple


class CreateUserRequest(NamedTuple):
    name: str
    email: str
