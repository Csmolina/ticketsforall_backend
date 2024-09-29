from typing import List, Optional
from core.src.models.user import User
from core.src.repositories.user_repository import UserRepository
from core.src.use_cases.user.get_all.response import GetAllUsersReponse


class GetAllUsers:
    def __init__(self, user_repository: UserRepository) -> None:
        self.user_repository = user_repository

    def __call__(self) -> Optional[List[User]]:
        users = self.user_repository.get_all_users()
        return GetAllUsersReponse(users=users)
