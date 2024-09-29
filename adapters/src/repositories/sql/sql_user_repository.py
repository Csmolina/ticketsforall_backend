from typing import List
from sqlalchemy.orm import Session
from core.src.repositories import UserRepository
from core.src.models import User
from core.src.exceptions import UserRepositoryException
from .tables import UserSchema


class SQLUserRepository(UserRepository):
    def __init__(self, session: Session) -> None:
        self.session = session

    def get_all_users(self) -> List[User]:
        try:
            with self.session as session:
                users = session.query(UserSchema).all()
                if not users:
                    return []
                user_list = [
                    User(
                        id=user.id,
                        name=str(user.name),
                        email=str(user.email),
                        user_type=str(user.user_type),
                    )
                    for user in users
                ]
                return user_list
        except Exception:
            self.session.rollback()
            raise UserRepositoryException(method="list")

    def create_user(self, name: str, email: str) -> User:
        try:
            user_to_create = UserSchema(
                name=name,
                email=email,
            )
            with self.session as session:
                session.add(user_to_create)
                session.commit()
                session.refresh(user_to_create)
                session.expunge(user_to_create)
            return User.model_validate(user_to_create)
        except Exception:
            self.session.rollback()
            raise UserRepositoryException(method="create")

    def get_by_email(self, email: str) -> User | None:
        try:
            with self.session as session:
                user = (
                    session.query(UserSchema).filter(UserSchema.email == email).first()
                )
                if not user:
                    return None
                return User(
                    id=str(user.id),
                    name=str(user.name),
                    email=str(user.email),
                    user_type=str(user.user_type),
                )
        except Exception:
            self.session.rollback()
            raise UserRepositoryException(method="find")

    def edit(self, user: User) -> User:
        try:
            with self.session as session:
                user_to_edit = (
                    session.query(UserSchema).filter(UserSchema.id == user.id).first()
                )
                user_to_edit.name = user.name
                user_to_edit.email = user.email
                user_to_edit.user_type = user.user_type
                session.commit()
            return user
        except Exception:
            self.session.rollback()
            raise UserRepositoryException(method="edit")
