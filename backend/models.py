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
    token_type: str = Field(default="bearer", description="The type of the token, typically 'bearer'")


# Pydantic model for user display in responses, without the password
class UserPublic(BaseModel):
    id: int
    username: str
    email: EmailStr
    created_at: datetime
