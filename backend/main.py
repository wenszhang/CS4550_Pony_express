from contextlib import asynccontextmanager
from datetime import datetime
from typing import Dict, List, Optional

from fastapi import FastAPI, HTTPException, status, Depends, Body, Query
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import joinedload
from sqlmodel import select, Session

from .auth import get_current_user, UserUpdate, auth_router
from .database import create_db_and_tables, get_session
from .models import UserPublic, ChatPublic, MessagePublic, MessageCreate
from .schema import UserInDB, ChatInDB, MessageInDB


@asynccontextmanager
async def lifespan(app: FastAPI):
    create_db_and_tables()
    yield


app = FastAPI(
    title="Assignment #1 - FastAPI backend",
    description="API for users and chat functions.",
    version="0.0.1",
    lifespan=lifespan
)

app.add_middleware(
    CORSMiddleware,  # type: ignore
    allow_origins=["http://localhost:5173"],  # URL of the frontend server
    allow_credentials=True,
    allow_methods=["*"],  # Allow all methods
    allow_headers=["*"],  # Allow all headers
)

app.include_router(auth_router, prefix="/auth")


# User routes ========================================

# GET /users
@app.get("/users", tags=["Users"], summary="Get all users",
         description="Retrieves a list of all users in the system",
         response_model=List[UserPublic])
async def get_users(session: Session = Depends(get_session)):
    users = session.exec(select(UserInDB)).all()
    result = [UserPublic.from_orm(user) for user in users]
    return {
        "meta": {
            "count": len(result)
        },
        "users": result
    }


# POST /auth/registration

# GET /users/{user_id}
@app.get("/users/{user_id}", tags=["Users"], summary="Get a user by ID",
         description="Fetches details of a user by ID",
         response_model=UserPublic)
async def get_user(user_id: int, session: Session = Depends(get_session)):
    user = session.exec(select(UserInDB).where(UserInDB.id == user_id)).first()
    if not user:
        raise HTTPException(
            status_code=404,
            detail={
                "type": "entity_not_found",
                "entity_name": "User",
                "entity_id": user_id
            }
        )
    return {"user": user}


# GET /users/{user_id}/chats
@app.get("/users/{user_id}/chats", tags=["Users"], summary="Get chats for a specific user",
         description="Retrieves a list of all chats that a user participates in",
         response_model=List[ChatPublic])
async def get_user_chats(user_id: int, session: Session = Depends(get_session)):
    user = session.get(UserInDB, user_id)
    if not user:
        raise HTTPException(
            status_code=404,
            detail={
                "type": "entity_not_found",
                "entity_name": "User",
                "entity_id": user_id
            }
        )

    result = session.exec(select(ChatInDB).where(ChatInDB.users.any(id=user_id))).all()  # type: ignore

    chats = [ChatPublic.from_orm(chat) for chat in result]

    return {
        "meta": {"count": len(chats)},
        "chats": chats
    }


# Helper function to validate datetime format
def is_valid_datetime(dt_str):
    try:
        datetime.fromisoformat(dt_str)
        return True
    except ValueError:
        return False


# GET /chats
@app.get("/chats", tags=["Chats"], summary="Get all chats",
         description="Retrieves a list of all chats",
         response_model=List[ChatPublic])
async def get_chats(session: Session = Depends(get_session)):
    result = session.exec(select(ChatInDB).options(joinedload(ChatInDB.owner))).all()

    chats = [ChatPublic.from_orm(chat) for chat in result]

    return {
        "meta": {"count": len(chats)},
        "chats": chats
    }


# GET /chats/{chat_id}
@app.get("/chats/{chat_id}", tags=["Chats"], summary="Get a chat by ID",
         description="Fetches details of a specific chat by ID")
async def get_chat(
        chat_id: int,
        include: Optional[List[str]] = Query(None),
        session: Session = Depends(get_session)
):
    # Check if chat exists
    chat = session.get(ChatInDB, chat_id)
    if not chat:
        raise HTTPException(
            status_code=404,
            detail={
                "type": "entity_not_found",
                "entity_name": "Chat",
                "entity_id": chat_id
            }
        )

    # Fetch chat metadata
    message_count = session.exec(select(MessageInDB).where(MessageInDB.chat_id == chat_id)).count()  # type: ignore
    user_count = session.exec(select(UserInDB).join(ChatInDB.users).where(ChatInDB.id == chat_id)).count()

    response = {
        "meta": {
            "message_count": message_count,
            "user_count": user_count
        },
        "chat": ChatPublic.from_orm(chat)
    }

    # Include messages if requested
    if 'messages' in (include or []):
        messages = session.exec(
            select(MessageInDB).where(MessageInDB.chat_id == chat_id).options(joinedload(MessageInDB.user))).all()
        response["messages"] = [MessagePublic.from_orm(msg) for msg in messages]

    # Include users if requested
    if 'users' in (include or []):
        users = session.exec(select(UserInDB).join(ChatInDB.users).where(ChatInDB.id == chat_id)).all()
        response["users"] = [UserPublic.from_orm(user) for user in users]

    return response


# PUT /chats/{chat_id}
@app.put("/chats/{chat_id}", tags=["Chats"], summary="Update a chat name by ID",
         description="Updates the name of an existing chat",
         response_model=ChatPublic)
async def update_chat(chat_id: int, update_data: Dict[str, str], session: Session = Depends(get_session)):
    chat = session.get(ChatInDB, chat_id)
    if not chat:
        raise HTTPException(status_code=404, detail={
            "type": "entity_not_found",
            "entity_name": "Chat",
            "entity_id": chat_id
        })

    if 'name' in update_data:
        chat.name = update_data['name']

    session.add(chat)
    session.commit()
    session.refresh(chat)

    return {"chat": chat}


# GET /chats/{chat_id}/messages
@app.get("/chats/{chat_id}/messages", tags=["Chats"], summary="Get messages for a specific chat",
         description="Retrieves all messages from a chat, identified by ID",
         response_model=List[MessagePublic])
async def get_chat_messages(chat_id: int, session: Session = Depends(get_session)):
    chat = session.get(ChatInDB, chat_id)
    if not chat:
        raise HTTPException(status_code=404, detail={
            "type": "entity_not_found",
            "entity_name": "Chat",
            "entity_id": chat_id
        })

    messages = session.exec(
        select(MessageInDB).where(MessageInDB.chat_id == chat_id).options(joinedload(MessageInDB.user))).all()
    result = [MessagePublic.from_orm(msg) for msg in messages]

    return {
        "meta": {
            "count": len(result),
        },
        "messages": result
    }


# GET /chats/{chat_id}/users
@app.get("/chats/{chat_id}/users", tags=["Chats"], summary="Get users in a specific chat",
         description="Fetches a list of users participating in a chat",
         response_model=List[UserPublic])
async def get_chat_users(chat_id: int, session: Session = Depends(get_session)):
    chat = session.get(ChatInDB, chat_id)
    if not chat:
        raise HTTPException(status_code=404, detail={
            "type": "entity_not_found",
            "entity_name": "Chat",
            "entity_id": chat_id
        })

    result = session.exec(select(UserInDB).where(ChatInDB.users.any(id=chat_id))).all()  # type: ignore

    users = [UserPublic.from_orm(user) for user in result]

    return {
        "meta": {
            "count": len(users),
        },
        "users": users
    }


# POST /chats
# @app.post("/chats", tags=["Chats"], summary="Create a new chat",
#           description="Creates a new chat with a unique ID",
#           status_code=status.HTTP_201_CREATED)
# async def create_chat(chat_data: Dict[str, str]):
#     chat_id = chat_data.get("id")
#     if chat_id in data["chats"]:
#         raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail={
#             "type": "duplicate_entity",
#             "entity_name": "Chat",
#             "entity_id": chat_id
#         })
#
#     chat_data['created_at'] = datetime.now().isoformat()
#     data["chats"][chat_id] = chat_data
#
#     return {"chat": data["chats"][chat_id]}

# New routes from A3 ========================================

@app.get("/users/me", tags=["Users"], summary="Get the current user",
         description="Returns the current user",
         response_model=UserPublic)
async def get_current_user_route(current_user: UserInDB = Depends(get_current_user)):
    if not current_user:
        raise HTTPException(status_code=404, detail="User not found")
    return current_user


@app.put("/users/me", tags=["Users"], summary="Update the current user",
         description="Updates the username or email of the current user",
         response_model=UserPublic)
async def update_current_user(
        update_data: UserUpdate = Body(...),
        current_user: UserInDB = Depends(get_current_user),
        session: Session = Depends(get_session)
):
    if update_data.username:
        existing_user = session.exec(select(UserInDB).where(UserInDB.username == update_data.username)).first()
        if existing_user and existing_user.id != current_user.id:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Username is already in use.")
        current_user.username = update_data.username

    if update_data.email:
        existing_user = session.exec(select(UserInDB).where(UserInDB.email == update_data.email)).first()
        if existing_user and existing_user.id != current_user.id:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email is already in use.")
        current_user.email = update_data.email

    session.add(current_user)
    session.commit()
    session.refresh(current_user)

    return {"user": current_user}


@app.post("/chats/{chat_id}/messages", tags=["Chats"], summary="Create a new message in a chat",
          description="Creates a new message in the chat, authored by the current user",
          response_model=MessagePublic, status_code=status.HTTP_201_CREATED)
async def create_message(
        chat_id: int,
        message_data: MessageCreate,
        current_user: UserInDB = Depends(get_current_user),
        session: Session = Depends(get_session)
):
    # Check if the chat exists
    chat = session.get(ChatInDB, chat_id)
    if not chat:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={
                "type": "entity_not_found",
                "entity_name": "Chat",
                "entity_id": chat_id
            }
        )

    # Create new message
    new_message = MessageInDB(
        text=message_data.text,
        chat_id=chat_id,
        user_id=current_user.id,
        created_at=datetime.utcnow()
    )

    session.add(new_message)
    session.commit()
    session.refresh(new_message)

    # Get the public representation of the message
    message_public = session.exec(
        select(MessageInDB).where(MessageInDB.id == new_message.id)
    ).first()

    return {"message": message_public}
