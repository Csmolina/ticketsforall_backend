from typing import List, NamedTuple

from core.src.models.user import User


class GetAllUsersReponse(NamedTuple):
    users: List[User]
