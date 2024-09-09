from adapters.src.repositories import (
    MemoryUserRepository,
    SQLUserRepository,
    SessionManager,
)
from core.src.repositories import UserRepository


def memory_user_repository() -> UserRepository:
    return MemoryUserRepository


def sql_user_repository() -> UserRepository:
    return SQLUserRepository(SessionManager.get_session())
