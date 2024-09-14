from pydantic import BaseModel, EmailStr
from typing import Optional


class User(BaseModel):
    id: int
    name: str
    email: EmailStr
    user_type: Optional[str] = "default"

    class Config:
        from_attributes = True
