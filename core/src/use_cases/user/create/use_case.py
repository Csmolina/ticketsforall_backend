from typing import Optional

from core.src.models import User
from core.src.exceptions import UserBusinessException
from core.src.repositories import UserRepository
from .request import CreateUserRequest
from .response import CreateUserResponse


class CreateUser:
    def __init__(self, user_repository: UserRepository) -> None:
        self.user_repository = user_repository

    def __call__(self, request: CreateUserRequest) -> Optional[CreateUserResponse]:
        user = User(**request._asdict())
        try:
            user_existing = self.user_repository.get_by_email(user.email)
            if not user_existing:
                response: Optional[User] = self.user_repository.create_user(user)
                return CreateUserResponse(response)

        except Exception as e:
            raise UserBusinessException(str(e))
