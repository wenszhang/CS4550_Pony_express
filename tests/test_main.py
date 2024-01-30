from fastapi.testclient import TestClient
from unittest import TestCase

from backend.main import app, load_data

client = TestClient(app)


class TestAPI(TestCase):
    def setUp(self):
        self.app = app
        self.app.state.data = load_data()
        self.client = TestClient(self.app)

    def tearDown(self):
        self.app.state.data = load_data()

    # [Tests for each route] ===============================

    def test_get_users(self):
        response = client.get("/users")
        self.assertEqual(200, response.status_code)
        self.assertIsInstance(response.json().get("meta"), dict)
        self.assertIsInstance(response.json().get("users"), list)

    def test_create_user(self):
        user_data = {"id": "testuser"}
        response = client.post("/users", json=user_data)
        self.assertEqual(200, response.status_code)
        self.assertEqual("testuser", response.json().get("user").get("id"))

    def test_get_user(self):
        user_id = "bishop"
        response = client.get(f"/users/{user_id}")
        self.assertEqual(200, response.status_code)
        self.assertEqual(user_id, response.json().get("user").get("id"))

    def test_get_user_chats(self):
        user_id = "bishop"
        response = client.get(f"/users/{user_id}/chats")
        self.assertEqual(200, response.status_code)
        self.assertIsInstance(response.json().get("chats"), list)

    def test_get_chats(self):
        response = client.get("/chats")
        self.assertEqual(200, response.status_code)
        self.assertIsInstance(response.json().get("chats"), list)

    def test_get_chat(self):
        chat_id = "660c7a6bc1324e4488cafabc59529c93"
        response = client.get(f"/chats/{chat_id}")
        self.assertEqual(200, response.status_code)
        self.assertEqual(chat_id, response.json().get("chat").get("id"))

    def test_update_chat(self):
        chat_id = "6215e6864e884132baa01f7f972400e2"
        updated_data = {"name": "New Chat Name"}
        response = client.put(f"/chats/{chat_id}", json=updated_data)
        self.assertEqual(200, response.status_code)
        self.assertEqual("New Chat Name", response.json().get("chat").get("name"))

    def test_delete_chat(self):
        chat_id = "660c7a6bc1324e4488cafabc59529c93"
        response = client.delete(f"/chats/{chat_id}")
        self.assertEqual(204, response.status_code)

    def test_get_chat_messages(self):
        chat_id = "660c7a6bc1324e4488cafabc59529c93"
        response = client.get(f"/chats/{chat_id}/messages")
        self.assertEqual(200, response.status_code)
        self.assertIsInstance(response.json().get("messages"), list)

    def test_get_chat_users(self):
        chat_id = "660c7a6bc1324e4488cafabc59529c93"
        response = client.get(f"/chats/{chat_id}/users")
        self.assertEqual(200, response.status_code)
        self.assertIsInstance(response.json().get("users"), list)

    # [Tests for invalid IDs] ===============================
    def test_get_user_invalid_id(self):
        response = client.get("/users/non_existing_user")
        self.assertEqual(404, response.status_code)

    def test_get_user_chats_invalid_id(self):
        response = client.get("/users/non_existing_user/chats")
        self.assertEqual(404, response.status_code)

    def test_get_chat_invalid_id(self):
        response = client.get("/chats/non_existing_chat")
        self.assertEqual(404, response.status_code)

    def test_update_chat_invalid_id(self):
        updated_data = {"name": "New Chat Name"}
        response = client.put("/chats/non_existing_chat", json=updated_data)
        self.assertEqual(404, response.status_code)

    def test_delete_chat_invalid_id(self):
        response = client.delete("/chats/non_existing_chat")
        self.assertEqual(404, response.status_code)

    def test_get_chat_messages_invalid_id(self):
        response = client.get("/chats/non_existing_chat/messages")
        self.assertEqual(404, response.status_code)

    def test_get_chat_users_invalid_id(self):
        response = client.get("/chats/non_existing_chat/users")
        self.assertEqual(404, response.status_code)

    # [Tests for duplicate IDs] ===============================
    def test_create_user_duplicate_id(self):
        # Create a new user
        user_data = {"id": "duplicate_user"}
        response = client.post("/users", json=user_data)
        self.assertEqual(200, response.status_code)

        # Try to create the same user again
        response = client.post("/users", json=user_data)
        self.assertEqual(422, response.status_code)
        self.assertIn("detail", response.json())
        self.assertEqual("duplicate_entity", response.json()["detail"]["type"])

    def test_create_chat_duplicate_id(self):
        # First, create a new chat
        chat_data = {"id": "duplicate_chat", "name": "Test Chat", "user_ids": ["user1"], "owner_id": "user1"}
        response = client.post("/chats", json=chat_data)
        self.assertEqual(201, response.status_code)

        # Try to create the same chat again
        response = client.post("/chats", json=chat_data)
        self.assertEqual(422, response.status_code)
        self.assertIn("detail", response.json())
        self.assertEqual("duplicate_entity", response.json()["detail"]["type"])
