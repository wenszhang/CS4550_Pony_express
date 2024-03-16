from pydantic import BaseModel, EmailStr, Field
from datetime import datetime


# Pydantic model for user registration
class UserCreate(BaseModel):
    username: str = Field(..., description="The unique username for the user")
    email: EmailStr = Field(..., description="The email address of the user")
    password: str = Field(..., description="The password for the user")


# Pydantic model for token responses
class Token(BaseModel):
    access_token: str = Field(..., description="The JWT token for access")
    token_type: str = Field(default="Bearer", description="The type of the token, typically 'bearer'")
    expires_in: int = Field(..., description="The lifetime of the token in seconds")


# Pydantic model for user display in responses, without the password
class UserPublic(BaseModel):
    id: int
    username: str
    email: str
    created_at: datetime

    class Config:
        orm_mode = True


class UserBase(BaseModel):
    id: int
    username: str
    email: str
    created_at: datetime


class ChatPublic(BaseModel):
    id: int
    name: str
    owner: UserBase
    created_at: datetime

    class Config:
        orm_mode = True


class MessagePublic(BaseModel):
    id: int
    text: str
    chat_id: int
    user: UserBase
    created_at: datetime

    class Config:
        orm_mode = True


class MessageCreate(BaseModel):
    text: str
