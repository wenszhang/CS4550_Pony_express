import os
from datetime import datetime, timedelta
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import JWTError, jwt
from passlib.context import CryptContext
from pydantic import BaseModel, EmailStr, Field
from sqlmodel import Session, select
from typing import Optional

from .database import get_session
from .schema import UserInDB
from .models import UserCreate, Token

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
access_token_duration = 30  # Minutes
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
jwt_key = os.environ.get("JWT_KEY", default="secret")
jwt_alg = "HS256"

# Todo: Finish implementing
auth_router = APIRouter()


# Models ========================================
class UserUpdate(BaseModel):
    username: Optional[str] = Field(None, description="The new username for the user")
    email: Optional[EmailStr] = Field(None, description="The new email address for the user")


# Methods ========================================
async def get_current_user(token: str = Depends(oauth2_scheme), session: Session = Depends(get_session)) -> UserInDB:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, jwt_key, algorithms=[jwt_alg])
        user_id: int = payload.get("sub")
        if user_id is None:
            raise credentials_exception
        user = session.exec(select(UserInDB).where(UserInDB.id == user_id)).first()
        if user is None:
            raise credentials_exception
        return user
    except JWTError:
        raise credentials_exception


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password):
    return pwd_context.hash(password)


def authenticate_user(session: Session, username: str, password: str):
    user = session.exec(select(UserInDB).where(UserInDB.username == username)).first()
    if not user or not verify_password(password, user.hashed_password):
        return False
    return user


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, jwt_key, algorithm=jwt_alg)
    return encoded_jwt


@auth_router.post("/auth/registration")
def register_user(user: UserCreate, session: Session = Depends(get_session)):
    db_user = session.exec(
        select(UserInDB).where((UserInDB.username == user.username) | (UserInDB.email == user.email))).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Username or email already registered")
    hashed_password = get_password_hash(user.password)
    db_user = UserInDB(username=user.username, email=user.email, hashed_password=hashed_password)
    session.add(db_user)
    session.commit()
    session.refresh(db_user)
    return {"username": db_user.username, "email": db_user.email}


@auth_router.post("/auth/token", response_model=Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(),
                                 session: Session = Depends(get_session)):
    user = authenticate_user(session, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=access_token_duration)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}
