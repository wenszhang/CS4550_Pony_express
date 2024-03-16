import os
from datetime import datetime, timedelta
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from passlib.context import CryptContext
from pydantic import BaseModel, Field
from sqlmodel import Session, select
from typing import Optional

from .database import get_session
from .schema import UserInDB
from .models import UserCreate, Token, UserPublic, UserResponse

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
access_token_duration = 3600  # seconds
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/token")
jwt_key = os.environ.get("JWT_KEY", default="secret")
jwt_alg = "HS256"

auth_router = APIRouter(prefix="/auth", tags=["Authentication"])


# Models ========================================
class UserUpdate(BaseModel):
    username: Optional[str] = Field(None, description="The new username for the user")
    email: Optional[str] = Field(None, description="The new email address for the user")


# Methods ========================================
async def get_current_user(token: str = Depends(oauth2_scheme), session: Session = Depends(get_session)) -> UserInDB:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail={
            "error": "invalid_client",
            "error_description": "invalid access token"
        },
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, jwt_key, algorithms=[jwt_alg])
        print(f"Decoded JWT payload: {payload}")
        user_id: int = int(payload.get("sub"))
        if user_id is None:
            raise credentials_exception
        user = session.exec(select(UserInDB).where(UserInDB.id == user_id)).first()
        print(f"Retrieved user: {user}")
        if user is None:
            raise credentials_exception
        return user
    except JWTError:
        raise credentials_exception


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    return pwd_context.hash(password)


def authenticate_user(session: Session, username: str, password: str) -> Optional[UserInDB]:
    user = session.exec(select(UserInDB).where(UserInDB.username == username)).first()
    if not user or not verify_password(password, user.hashed_password):
        return None
    return user


def create_access_token(*, data: dict, expires_delta: timedelta):
    to_encode = data.copy()
    expire = datetime.utcnow() + expires_delta
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, jwt_key, algorithm=jwt_alg)
    return encoded_jwt


# Auth routes ========================================

# POST /auth/registration
@auth_router.post("/registration", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
def register_user(
        user: UserCreate,
        session: Session = Depends(get_session)
):
    # Check if username or email already exists
    existing_user_username = session.exec(
        select(UserInDB).where(UserInDB.username == user.username)
    ).first()
    existing_user_email = session.exec(
        select(UserInDB).where(UserInDB.email == user.email)
    ).first()

    # If username or email is taken, respond with a 422 error
    if existing_user_username:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail={
                "type": "duplicate_value",
                "entity_name": "User",
                "entity_field": "username",
                "entity_value": user.username
            }
        )
    if existing_user_email:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail={
                "type": "duplicate_value",
                "entity_name": "User",
                "entity_field": "email",
                "entity_value": user.email
            }
        )

    # Hash the password
    hashed_password = get_password_hash(user.password)

    # Create new user instance
    new_user = UserInDB(
        username=user.username,
        email=user.email,
        hashed_password=hashed_password
    )

    # Add to the database
    session.add(new_user)
    session.commit()
    session.refresh(new_user)

    # Return the public view of the user
    return UserResponse(user=UserPublic.from_orm(new_user))


# POST /auth/token
@auth_router.post("/token", response_model=Token)
async def login_for_access_token(
        form_data: OAuth2PasswordRequestForm = Depends(),
        session: Session = Depends(get_session)
):
    user = authenticate_user(session, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail={
                "error": "invalid_client",
                "error_description": "invalid username or password"
            },
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token_expires = timedelta(seconds=access_token_duration)
    access_token = create_access_token(
        data={"sub": str(user.id)}, expires_delta=access_token_expires
    )
    return {
        "access_token": access_token,
        "token_type": "Bearer",
        "expires_in": access_token_duration
    }
