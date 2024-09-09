from typing import List, Optional
from core.src.repositories import UserRepository
from core.src.models import User
from core.src.exceptions import UserRepositoryException


class MemoryUserRepository(UserRepository):
    users: List[User]

    def __init__(self) -> None:
        self.users = []

    def create(self, user: User) -> User:
        try:
            self.users.append(user)
            return user
        except Exception:
            raise UserRepositoryException(method="create")

    def get_by_email(self, email: str) -> Optional[User]:
        try:
            return next((user for user in self.users if user.email == email), None)
        except Exception:
            raise UserRepositoryException(method="get_by_email")
