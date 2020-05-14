import json
import pytest
from app.api import message_crud
from tests.config import *

# # POST
def test_create_message(test_app, monkeypatch):
    test_request_payload = CORRECT_PAYLOAD_MESSAGE1
    test_response_payload = CORRECT_POST_RESPONSE

    async def mock_post(payload):
        return 1

    monkeypatch.setattr(message_crud, "post", mock_post)

    response = test_app.post("/messages/", data=json.dumps(test_request_payload),)

    assert response.status_code == 201
    assert response.json() == test_response_payload


def test_create_message_invalid_json(test_app):
    response = test_app.post("/messages/", data=json.dumps(INCORRECT_JSON_MESSAGES),)
    assert response.status_code == 422


# # GET
def test_read_message(test_app, monkeypatch):
    test_data = GET_READ_MESSAGE

    async def mock_get(id):
        return test_data

    monkeypatch.setattr(message_crud, "get", mock_get)

    response = test_app.get("/messages/1")
    assert response.status_code == 200
    assert response.json() == test_data


def test_read_message_incorrect_id(test_app, monkeypatch):
    async def mock_get(id):
        return None

    monkeypatch.setattr(message_crud, "get", mock_get)

    response = test_app.get("/messages/999")
    assert response.status_code == 404
    assert response.json()["Error"] == "message NOT found"

    response = test_app.get("/messages/0")
    assert response.status_code == 422


def test_read_all_messages(test_app, monkeypatch):
    test_data = [
        {**CORRECT_PAYLOAD_MESSAGE1, **{"id": 1}},
        {**CORRECT_PAYLOAD_MESSAGE2, **{"id": 2}},
    ]

    async def mock_get_all():
        return test_data

    monkeypatch.setattr(message_crud, "get_all", mock_get_all)

    response = test_app.get("/messages/")

    assert response.status_code == 200
    assert response.json() == test_data


# # PUT
def test_update_message(test_app, monkeypatch):
    test_update_data = {**CORRECT_PAYLOAD_MESSAGE1, **{"id": 1}}

    async def mock_get(id):
        return True

    monkeypatch.setattr(message_crud, "get", mock_get)

    async def mock_put(id, payload):
        return 1

    monkeypatch.setattr(message_crud, "put", mock_put)

    response = test_app.put("/messages/1/", data=json.dumps(test_update_data))
    assert response.status_code == 200
    assert response.json() == test_update_data


@pytest.mark.parametrize(
    "id, payload, status_code",
    [  # empty
        [1, {}, 422],
        # incorrect field
        [1, INCORRECT_JSON_MESSAGES, 422,],
        [
            # not found
            999,
            CORRECT_PAYLOAD_MESSAGE1,
            404,
        ],
        # Not found and 0
        [0, CORRECT_PAYLOAD_MESSAGE2, 422,],
    ],
)
def test_update_message_invalid(test_app, monkeypatch, id, payload, status_code):
    async def mock_get(id):
        return None

    monkeypatch.setattr(message_crud, "get", mock_get)

    response = test_app.put(f"/messages/{id}/", data=json.dumps(payload),)
    assert response.status_code == status_code


# # DELETE
def test_remove_messages(test_app, monkeypatch):
    test_data = {**CORRECT_PAYLOAD_MESSAGE1, **{"id": 1}}

    async def mock_get(id):
        return test_data

    monkeypatch.setattr(message_crud, "get", mock_get)

    async def mock_delete(id):
        return id

    monkeypatch.setattr(message_crud, "delete", mock_delete)

    response = test_app.delete("/messages/1/")
    assert response.status_code == 200
    assert response.json() == test_data


def test_remove_messages_incorrect_id(test_app, monkeypatch):
    async def mock_get(id):
        return None

    monkeypatch.setattr(message_crud, "get", mock_get)

    response = test_app.delete("/messages/999/")
    assert response.status_code == 404
    assert response.json()["Error"] == "message NOT found"

    response = test_app.delete("/messages/0/")
    assert response.status_code == 422
