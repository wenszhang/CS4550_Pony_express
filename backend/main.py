from fastapi import FastAPI, HTTPException, status
from typing import List, Dict
from datetime import datetime
import json

from fastapi.openapi.models import Response

app = FastAPI(
    title="Assignment #1 - FastAPI backend",
    description="API for users and chat functions.",
    version="0.0.1"
)

# Load data from fake_db.json
with open('fake_db.json', 'r') as file:
    data = json.load(file)


# Helper function to get current datetime in ISO format
def current_iso_datetime():
    return datetime.now().isoformat()


# GET /users
@app.get("/users", tags=["Users"], summary="Get all users")
async def get_users():
    users = sorted(data.get('users', {}).values(), key=lambda x: x['id'])
    return {
        "meta": {
            "count": len(users)
        },
        "users": users
    }


# POST /users
@app.post("/users", tags=["Users"], summary="Create a new user")
async def create_user(user: Dict[str, str]):
    user_id = user.get("id")
    if user_id in data["users"]:
        raise HTTPException(status_code=422, detail={
            "type": "duplicate_entity",
            "entity_name": "User",
            "entity_id": user_id
        })

    created_at = current_iso_datetime()
    data["users"][user_id] = {
        "id": user_id,
        "created_at": created_at
    }
    return {
        "user": data["users"][user_id]
    }


# GET /users/{user_id}
@app.get("/users/{user_id}", tags=["Users"], summary="Get a user by ID")
async def get_user(user_id: str):
    user = data["users"].get(user_id)
    if not user:
        raise HTTPException(status_code=404, detail={
            "type": "entity_not_found",
            "entity_name": "User",
            "entity_id": user_id
        })
    return {"user": user}


# GET /users/{user_id}/chats
@app.get("/users/{user_id}/chats", tags=["Chats"], summary="Get chats for a specific user")
async def get_user_chats(user_id: str):
    if user_id not in data["users"]:
        raise HTTPException(status_code=404, detail={
            "type": "entity_not_found",
            "entity_name": "User",
            "entity_id": user_id
        })

    chats = [chat for chat in data.get('chats', {}).values() if user_id in chat['user_ids']]
    chats = sorted(chats, key=lambda x: x['name'])
    return {
        "meta": {
            "count": len(chats)
        },
        "chats": chats
    }


# GET /chats
@app.get("/chats", tags=["Chats"], summary="Get all chats")
async def get_chats():
    chats = sorted(data.get('chats', {}).values(), key=lambda x: x['name'])
    return {
        "meta": {
            "count": len(chats)
        },
        "chats": chats
    }


# GET /chats/{chat_id}
@app.get("/chats/{chat_id}", tags=["Chats"], summary="Get a chat by ID")
async def get_chat(chat_id: str):
    chat = data["chats"].get(chat_id)
    if not chat:
        raise HTTPException(status_code=404, detail={
            "type": "entity_not_found",
            "entity_name": "Chat",
            "entity_id": chat_id
        })
    return {"chat": chat}


# PUT /chats/{chat_id}
@app.put("/chats/{chat_id}", tags=["Chats"], summary="Update a chat name by ID")
async def update_chat(chat_id: str, update_data: Dict[str, str]):
    chat = data["chats"].get(chat_id)
    if not chat:
        raise HTTPException(status_code=404, detail={
            "type": "entity_not_found",
            "entity_name": "Chat",
            "entity_id": chat_id
        })
    chat["name"] = update_data.get("name", chat["name"])
    return {"chat": chat}


@app.delete("/chats/{chat_id}", tags=["Chats"], summary="Delete a chat by ID")
async def delete_chat(chat_id: str):
    if chat_id not in data["chats"]:
        raise HTTPException(status_code=404, detail={
            "type": "entity_not_found",
            "entity_name": "Chat",
            "entity_id": chat_id
        })
    del data["chats"][chat_id]
    return Response(status_code=status.HTTP_204_NO_CONTENT)


# GET /chats/{chat_id}/messages
@app.get("/chats/{chat_id}/messages", tags=["Chats"], summary="Get messages for a specific chat")
async def get_chat_messages(chat_id: str):
    if chat_id not in data["chats"]:
        raise HTTPException(status_code=404, detail={
            "type": "entity_not_found",
            "entity_name": "Chat",
            "entity_id": chat_id
        })
    messages = sorted(data["chats"][chat_id].get("messages", []),
                      key=lambda x: x['created_at'])
    return {
        "meta": {
            "count": len(messages),
        },
        "messages": messages
    }


# GET /chats/{chat_id}/users
@app.get("/chats/{chat_id}/users", tags=["Chats"], summary="Get users in a specific chat")
async def get_chat_users(chat_id: str):
    if chat_id not in data["chats"]:
        raise HTTPException(status_code=404, detail={
            "type": "entity_not_found",
            "entity_name": "Chat",
            "entity_id": chat_id
        })
    user_ids = data["chats"][chat_id].get("user_ids", [])
    users = [data["users"][uid] for uid in user_ids if uid in data["users"]]
    users_sorted = sorted(users, key=lambda x: x['id'])
    return {
        "meta": {
            "count": len(users_sorted),
        },
        "users": users_sorted
    }
