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
        try:
            user_existing = self.user_repository.get_by_email(request.email)
            if not user_existing:
                new_user: Optional[User] = self.user_repository.create_user(
                    name=request.name, email=request.email
                )
                return CreateUserResponse(user=new_user)
            return CreateUserResponse(user=user_existing)

        except Exception as e:
            raise UserBusinessException(str(e))
