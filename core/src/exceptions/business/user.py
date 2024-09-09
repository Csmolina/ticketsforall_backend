from .base import BusinessException, NotFoundException, NoneException


class UserBusinessException(BusinessException):
    """User Business Exception"""


class UserNotFoundException(NotFoundException):
    def __init__(self, user_mail: str):
        super().__init__(entity_type="User", entity_id=user_mail)


class UserNoneException(NoneException):
    def __init__(self) -> None:
        super().__init__(entity_type="User")
