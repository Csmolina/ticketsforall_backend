import pytest
from unittest.mock import Mock

from core.src.use_cases.user.create.use_case import CreateUser

from core.src.use_cases.user.create.request import CreateUserRequest


from core.src.models import User

from core.src.exceptions import UserBusinessException
from core.src.repositories import UserRepository


def test_create_user_success():
    user_repository = Mock(spec=UserRepository)
    user_repository.get_by_email.return_value = None
    user_repository.create_user.return_value = User(
        id=1, name="John Doe", email="john.doe@example.com", user_type="default"
    )

    create_user = CreateUser(user_repository)
    request = CreateUserRequest(name="John Doe", email="john.doe@example.com")

    response = create_user(request)

    assert response.user.name == "John Doe"
    assert response.user.email == "john.doe@example.com"
    user_repository.get_by_email.assert_called_once_with("john.doe@example.com")
    user_repository.create_user.assert_called_once_with(
        name="John Doe", email="john.doe@example.com"
    )


def test_create_user_already_exists():
    existing_user = User(
        id=1, name="Jane Doe", email="jane.doe@example.com", user_type="default"
    )
    user_repository = Mock(spec=UserRepository)
    user_repository.get_by_email.return_value = existing_user

    create_user = CreateUser(user_repository)
    request = CreateUserRequest(name="Jane Doe", email="jane.doe@example.com")

    response = create_user(request)

    assert response.user == existing_user
    user_repository.get_by_email.assert_called_once_with("jane.doe@example.com")
    user_repository.create_user.assert_not_called()


def test_create_user_exception():

    user_repository = Mock(spec=UserRepository)
    user_repository.get_by_email.side_effect = Exception("Database error")

    create_user = CreateUser(user_repository)
    request = CreateUserRequest(name="John Doe", email="john.doe@example.com")

    with pytest.raises(UserBusinessException) as exc_info:
        create_user(request)

    assert str(exc_info.value) == "Database error"
    user_repository.get_by_email.assert_called_once_with("john.doe@example.com")
    user_repository.create_user.assert_not_called()
