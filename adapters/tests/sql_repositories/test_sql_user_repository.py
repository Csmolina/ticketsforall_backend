import pytest

from unittest.mock import MagicMock, patch
from adapters.src.repositories import SQLUserRepository
from adapters.src.repositories.sql.tables.user import UserSchema
from core.src.exceptions.repository.user import UserRepositoryException
from core.src.models.user import User


def test_create_user_success():
    # Arrange
    mock_session = MagicMock()
    repo = SQLUserRepository(session=mock_session)

    # Mock UserSchema and User.model_validate to return a dummy user
    mock_user_to_create = UserSchema(name="Test User", email="test@example.com")
    mock_user_to_create.id = 1
    mock_user_to_create.user_type = "default"
    mock_user = User.model_validate(mock_user_to_create)

    with patch(
        "adapters.src.repositories.UserSchema", return_value=mock_user_to_create
    ), patch("core.src.models.User.model_validate", return_value=mock_user):
        # Mock session behavior
        mock_session.add = MagicMock()
        mock_session.commit = MagicMock()
        mock_session.refresh = MagicMock()
        mock_session.expunge = MagicMock()

        # Act
        result = repo.create_user(name="Test User", email="test@example.com")

        assert result == mock_user


def test_create_user_exception_handling():
    # Arrange
    mock_session = MagicMock()
    repo = SQLUserRepository(session=mock_session)
    user = UserSchema(name="Test User", email="test@example.com")
    with patch("adapters.src.repositories.UserSchema", return_value=user):
        # Mock session behavior
        repo.session.add = MagicMock()
        repo.session.commit = MagicMock(side_effect=Exception("Database error"))
        repo.session.refresh = MagicMock()
        repo.session.expunge = MagicMock()

        # Act & Assert
        with pytest.raises(UserRepositoryException):
            repo.create_user(name="Test User", email="test@example.com")

        # Ensure rollback was called
        mock_session.rollback.assert_called_once()


def test_get_all_users_success():
    mock_session = MagicMock()
    mock_users = [
        UserSchema(id=1, name="User 1", email="user1@example.com", user_type="default"),
        UserSchema(id=2, name="User 2", email="user2@example.com", user_type="default"),
    ]

    mock_session.__enter__.return_value = mock_session

    mock_session.query.return_value.all.return_value = mock_users

    repo = SQLUserRepository(session=mock_session)

    expected_users = [
        User(id=1, name="User 1", email="user1@example.com", user_type="default"),
        User(id=2, name="User 2", email="user2@example.com", user_type="default"),
    ]

    result = repo.get_all_users()

    assert result == expected_users

    mock_session.query.assert_called_once_with(UserSchema)


def test_get_all_users_empty():
    mock_session = MagicMock()
    repo = SQLUserRepository(session=mock_session)

    mock_query = mock_session.query.return_value
    mock_query.all.return_value = []

    result = repo.get_all_users()

    assert result == []


def test_get_all_users_exception():
    mock_session = MagicMock()
    repo = SQLUserRepository(session=mock_session)

    mock_session.__enter__.return_value.query.side_effect = Exception("Database error")

    with pytest.raises(UserRepositoryException):
        repo.get_all_users()
    mock_session.rollback.assert_called_once()
