import json
import os
from datetime import datetime
from typing import Dict
from fastapi import FastAPI, HTTPException, Response, status
from fastapi.middleware.cors import CORSMiddleware


def load_data():
    backend_dir = os.path.dirname(os.path.abspath(__file__))
    fake_db_path = os.path.join(backend_dir, 'fake_db.json')
    with open(fake_db_path, 'r') as file:
        return json.load(file)


app = FastAPI(
    title="Assignment #1 - FastAPI backend",
    description="API for users and chat functions.",
    version="0.0.1"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],  # URL of the frontend server
    allow_credentials=True,
    allow_methods=["*"],  # Allow all methods
    allow_headers=["*"],  # Allow all headers
)

# Load data on app startup
data = load_data()


# Helper function to get current datetime in ISO format
def current_iso_datetime():
    return datetime.now().isoformat()


# GET /users
@app.get("/users", tags=["Users"], summary="Get all users",
         description="Retrieves a list of all users in the system")
async def get_users():
    users = sorted(data.get('users', {}).values(), key=lambda x: x['id'])
    return {
        "meta": {
            "count": len(users)
        },
        "users": users
    }


# POST /users
@app.post("/users", tags=["Users"], summary="Create a new user",
          description="Creates a new user with a unique ID")
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
@app.get("/users/{user_id}", tags=["Users"], summary="Get a user by ID",
         description="Fetches details of a user by ID")
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
@app.get("/users/{user_id}/chats", tags=["Users"], summary="Get chats for a specific user",
         description="Retrieves a list of all chats that a user participates in")
async def get_user_chats(user_id: str):
    if user_id not in data["users"]:
        raise HTTPException(status_code=404, detail={
            "type": "entity_not_found",
            "entity_name": "User",
            "entity_id": user_id
        })

    user_chats = [
        {
            "id": chat["id"],
            "name": chat["name"],
            "user_ids": chat["user_ids"],
            "owner_id": chat["owner_id"],
            "created_at": chat["created_at"]
        }
        for chat in data.get('chats', {}).values() if user_id in chat['user_ids']
    ]

    user_chats = sorted(user_chats, key=lambda x: x['name'])
    return {
        "meta": {"count": len(user_chats)},
        "chats": user_chats
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
         description="Retrieves a list of all chats")
async def get_chats():
    chats = data.get('chats', {}).values()

    # Validate and format chats
    formatted_chats = []
    for chat in chats:
        if all(k in chat for k in ["id", "name", "user_ids", "owner_id", "created_at"]) and is_valid_datetime(
                chat["created_at"]):
            formatted_chats.append({
                "id": chat["id"],
                "name": chat["name"],
                "user_ids": chat["user_ids"],
                "owner_id": chat["owner_id"],
                "created_at": chat["created_at"]
            })
        else:
            pass

    sorted_chats = sorted(formatted_chats, key=lambda x: x['name'])
    return {
        "meta": {"count": len(sorted_chats)},
        "chats": sorted_chats
    }


# GET /chats/{chat_id}
@app.get("/chats/{chat_id}", tags=["Chats"], summary="Get a chat by ID",
         description="Fetches details of a specific chat by ID")
async def get_chat(chat_id: str):
    chat = data["chats"].get(chat_id)
    if not chat:
        raise HTTPException(status_code=404, detail={
            "type": "entity_not_found",
            "entity_name": "Chat",
            "entity_id": chat_id
        })

    # Check for required fields
    required_fields = ["id", "name", "user_ids", "owner_id", "created_at"]
    if all(field in chat for field in required_fields):
        return {"chat": {field: chat[field] for field in required_fields}}
    else:
        raise HTTPException(status_code=500, detail="Chat data structure is incorrect")


# PUT /chats/{chat_id}
@app.put("/chats/{chat_id}", tags=["Chats"], summary="Update a chat name by ID",
         description="Updates the name of an existing chat")
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


# DELETE /chats/{chat_id}
@app.delete("/chats/{chat_id}", tags=["Chats"], summary="Delete a chat by ID",
            description="Deletes a chat from the system by ID")
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
@app.get("/chats/{chat_id}/messages", tags=["Chats"], summary="Get messages for a specific chat",
         description="Retrieves all messages from a chat, identified by ID")
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
@app.get("/chats/{chat_id}/users", tags=["Chats"], summary="Get users in a specific chat",
         description="Fetches a list of users participating in a chat")
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


# POST /chats
@app.post("/chats", tags=["Chats"], summary="Create a new chat",
          description="Creates a new chat with a unique ID",
          status_code=status.HTTP_201_CREATED)
async def create_chat(chat_data: Dict[str, str]):
    chat_id = chat_data.get("id")
    if chat_id in data["chats"]:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail={
            "type": "duplicate_entity",
            "entity_name": "Chat",
            "entity_id": chat_id
        })

    chat_data['created_at'] = current_iso_datetime()
    data["chats"][chat_id] = chat_data

    return {"chat": data["chats"][chat_id]}
