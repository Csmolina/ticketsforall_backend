from pydantic import BaseModel
from typing import Optional


class User(BaseModel):
    id: int
    name: str
    email: str
    user_type: Optional[str] = "default"

    class Config:
        from_attributes = True  # This replaces `orm_mode` in Pydantic v2
