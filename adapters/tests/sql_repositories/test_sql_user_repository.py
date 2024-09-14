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
