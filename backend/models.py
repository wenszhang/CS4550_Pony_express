from typing import List

from pydantic import BaseModel
from datetime import datetime


# Pydantic model for user registration
class UserCreate(BaseModel):
    username: str
    email: str
    password: str


# Pydantic model for token responses
class Token(BaseModel):
    access_token: str
    token_type: str
    expires_in: int


# Pydantic model for user display in responses, without the password
class UserPublic(BaseModel):
    id: int
    username: str
    email: str
    created_at: datetime

    class Config:
        orm_mode = True
        from_attributes = True


class UserBase(BaseModel):
    id: int
    username: str
    email: str
    created_at: datetime

    class Config:
        orm_mode = True
        from_attributes = True


class ChatPublic(BaseModel):
    id: int
    name: str
    owner: UserBase
    created_at: datetime

    class Config:
        orm_mode = True
        from_attributes = True


class MessagePublic(BaseModel):
    id: int
    text: str
    chat_id: int
    user: UserBase
    created_at: datetime

    class Config:
        orm_mode = True
        from_attributes = True


class MessageCreate(BaseModel):
    text: str


# Assuming Meta is another Pydantic model you've defined to encapsulate meta information
class Meta(BaseModel):
    count: int


# The UsersResponse model will include both the meta information and the users list
class UsersResponse(BaseModel):
    meta: Meta
    users: List[UserPublic]
