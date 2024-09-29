from core.src.repositories import UserRepository
from core.src.use_cases.user.get_all.use_case import GetAllUsers
from factories.repositories import sql_user_repository
from core.src.use_cases import CreateUser


def get_user_repository() -> UserRepository:
    return sql_user_repository()


def get_or_create_user_use_case() -> CreateUser:
    return CreateUser(get_user_repository())


def get_all_users_use_case() -> GetAllUsers:
    return GetAllUsers(get_user_repository())
