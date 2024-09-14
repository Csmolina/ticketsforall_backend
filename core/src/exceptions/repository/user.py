from .base import RepositoryException


class UserRepositoryException(RepositoryException):
    def __init__(self, method: str):
        super().__init__(entity_type="User", method=method)
