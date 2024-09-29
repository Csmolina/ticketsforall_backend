from unittest.mock import MagicMock
from core.src.models.user import User
from core.src.repositories.user_repository import UserRepository
from core.src.use_cases.user.get_all.use_case import GetAllUsers
from core.src.use_cases.user.get_all.response import GetAllUsersReponse


def test_get_all_users():
    mock_user_repository = MagicMock(spec=UserRepository)
    mock_users = [
        User(id=1, name="John Doe", email="test@gmail.com", user_type="default"),
        User(id=2, name="Jane Doe", email="test@gmail.com", user_type="default"),
    ]
    mock_user_repository.get_all_users.return_value = mock_users
    use_case = GetAllUsers(user_repository=mock_user_repository)

    response = use_case()

    assert isinstance(response, GetAllUsersReponse)
    assert response.users == mock_users
    mock_user_repository.get_all_users.assert_called_once()


def test_get_all_users_empty():

    mock_user_repository = MagicMock(spec=UserRepository)
    mock_user_repository.get_all_users.return_value = []
    use_case = GetAllUsers(user_repository=mock_user_repository)

    response = use_case()

    assert isinstance(response, GetAllUsersReponse)
    assert response.users == []
    mock_user_repository.get_all_users.assert_called_once()
