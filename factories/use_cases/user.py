from core.src.repositories import UserRepository
from factories.repositories import sql_user_repository
from core.src.use_cases import CreateUser


def get_user_repository() -> UserRepository:
    return sql_user_repository()


def get_or_create_user_use_case() -> CreateUser:
    return CreateUser(get_user_repository())
