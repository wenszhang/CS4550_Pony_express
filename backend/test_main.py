from fastapi.testclient import TestClient
from unittest import TestCase
from main import app  # Import your FastAPI app

client = TestClient(app)


class TestAPI(TestCase):

    # [Tests for each route] ===============================

    def test_get_users(self):
        response = client.get("/users")
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.json().get("meta"), dict)
        self.assertIsInstance(response.json().get("users"), list)

    def test_create_user(self):
        user_data = {"id": "testuser"}
        response = client.post("/users", json=user_data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json().get("user").get("id"), "testuser")
        # TODO: Additional checks for the 'created_at' field

    def test_get_user(self):
        user_id = "bishop"
        response = client.get(f"/users/{user_id}")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json().get("user").get("id"), user_id)

    def test_get_user_chats(self):
        user_id = "bishop"
        response = client.get(f"/users/{user_id}/chats")
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.json().get("chats"), list)

    def test_get_chats(self):
        response = client.get("/chats")
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.json().get("chats"), list)

    def test_get_chat(self):
        chat_id = "643c31c6c9c640f6a73317e9ed7abe34"  # Need valid chat ID
        response = client.get(f"/chats/{chat_id}")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json().get("chat").get("id"), chat_id)

    def test_update_chat(self):
        chat_id = "643c31c6c9c640f6a73317e9ed7abe34"  # Replace with a valid chat ID
        updated_data = {"name": "New Chat Name"}
        response = client.put(f"/chats/{chat_id}", json=updated_data)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json().get("chat").get("name"), "New Chat Name")

    def test_delete_chat(self):
        chat_id = "643c31c6c9c640f6a73317e9ed7abe34"  # Replace with a valid chat ID
        response = client.delete(f"/chats/{chat_id}")
        self.assertEqual(response.status_code, 204)
        # TODO: verify the chat has been deleted with a follow-up GET request

    def test_get_chat_messages(self):
        chat_id = "643c31c6c9c640f6a73317e9ed7abe34"  # Replace with a valid chat ID
        response = client.get(f"/chats/{chat_id}/messages")
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.json().get("messages"), list)

    def test_get_chat_users(self):
        chat_id = "643c31c6c9c640f6a73317e9ed7abe34"  # Replace with a valid chat ID
        response = client.get(f"/chats/{chat_id}/users")
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.json().get("users"), list)

    # [Tests for invalid IDs] ===============================
    def test_get_user_invalid_id(self):
        response = client.get("/users/non_existing_user")
        self.assertEqual(response.status_code, 404)

    def test_get_user_chats_invalid_id(self):
        response = client.get("/users/non_existing_user/chats")
        self.assertEqual(response.status_code, 404)

    def test_get_chat_invalid_id(self):
        response = client.get("/chats/non_existing_chat")
        self.assertEqual(response.status_code, 404)

    def test_update_chat_invalid_id(self):
        updated_data = {"name": "New Chat Name"}
        response = client.put("/chats/non_existing_chat", json=updated_data)
        self.assertEqual(response.status_code, 404)

    def test_delete_chat_invalid_id(self):
        response = client.delete("/chats/non_existing_chat")
        self.assertEqual(response.status_code, 404)

    def test_get_chat_messages_invalid_id(self):
        response = client.get("/chats/non_existing_chat/messages")
        self.assertEqual(response.status_code, 404)

    def test_get_chat_users_invalid_id(self):
        response = client.get("/chats/non_existing_chat/users")
        self.assertEqual(response.status_code, 404)

    # [Tests for duplicate IDs] ===============================
    def test_create_user_duplicate_id(self):
        # Create a new user
        user_data = {"id": "duplicate_user"}
        response = client.post("/users", json=user_data)
        self.assertEqual(response.status_code, 200)

        # Try to create the same user again
        response = client.post("/users", json=user_data)
        self.assertEqual(response.status_code, 422)
        self.assertIn("detail", response.json())
        self.assertEqual(response.json()["detail"]["type"], "duplicate_entity")

    def test_create_chat_duplicate_id(self):
        # First, create a new chat
        chat_data = {"id": "duplicate_chat", "name": "Test Chat", "user_ids": ["user1"], "owner_id": "user1"}
        response = client.post("/chats", json=chat_data)
        self.assertEqual(response.status_code, 200)

        # Try to create the same chat again
        response = client.post("/chats", json=chat_data)
        self.assertEqual(response.status_code, 422)
        self.assertIn("detail", response.json())
        self.assertEqual(response.json()["detail"]["type"], "duplicate_entity")
