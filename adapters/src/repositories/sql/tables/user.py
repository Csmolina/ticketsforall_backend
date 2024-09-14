from sqlalchemy import Column, Integer, String
from .base import Base


class UserSchema(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String, index=True)
    email = Column(String, unique=True, index=True)
    user_type = Column(String, default="default")
