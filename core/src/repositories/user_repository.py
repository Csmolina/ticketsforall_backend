from abc import ABC, abstractmethod
from typing import List, Optional
from core.src.models import User


class UserRepository(ABC):
    @abstractmethod
    def get_by_email(self, email: str) -> Optional[User]:
        pass

    @abstractmethod
    def create_user(self, name: str, email: str) -> User:
        pass

    @abstractmethod
    def get_all_users(self) -> Optional[List[User]]:
        pass
