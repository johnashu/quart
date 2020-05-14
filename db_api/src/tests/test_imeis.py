import json
import pytest
from app.api import blog_crud

# POST
def test_create_blog(test_app, monkeypatch):
    test_request_payload = {"blog": "123456789012345"}
    test_response_payload = {"id": 1, "blog": "123456789012345"}

    async def mock_post(payload):
        return 1

    monkeypatch.setattr(blog_crud, "post", mock_post)

    response = test_app.post("/blog/", data=json.dumps(test_request_payload),)

    assert response.status_code == 201
    assert response.json() == test_response_payload


def test_create_blog_invalid_json(test_app):
    response = test_app.post("/blog/", data=json.dumps({"iccid": 123456789012345}),)
    assert response.status_code == 422


# GET
def test_read_blog(test_app, monkeypatch):
    test_data = {"id": 1, "blog": "123456789012345"}

    async def mock_get(id):
        return test_data

    monkeypatch.setattr(blog_crud, "get", mock_get)

    response = test_app.get("/blog/1")
    assert response.status_code == 200
    assert response.json() == test_data


def test_read_blog_incorrect_id(test_app, monkeypatch):
    async def mock_get(id):
        return None

    monkeypatch.setattr(blog_crud, "get", mock_get)

    response = test_app.get("/blog/999")
    assert response.status_code == 404
    assert response.json()["Error"] == "blog NOT found"

    response = test_app.get("/blog/0")
    assert response.status_code == 422


def test_read_all_blog(test_app, monkeypatch):
    test_data = [
        {"id": 1, "blog": "123456789012345"},
        {"id": 2, "blog": "999996789034345"},
    ]

    async def mock_get_all():
        return test_data

    monkeypatch.setattr(blog_crud, "get_all", mock_get_all)

    response = test_app.get("/blog/")
    assert response.status_code == 200
    assert response.json() == test_data


# PUT
def test_update_blog(test_app, monkeypatch):
    test_update_data = {"id": 1, "blog": "999996789034345"}

    async def mock_get(id):
        return True

    monkeypatch.setattr(blog_crud, "get", mock_get)

    async def mock_put(id, payload):
        return 1

    monkeypatch.setattr(blog_crud, "put", mock_put)

    response = test_app.put("/blog/1/", data=json.dumps(test_update_data))
    assert response.status_code == 200
    assert response.json() == test_update_data


@pytest.mark.parametrize(
    "id, payload, status_code",
    [
        [1, {}, 422],
        [1, {"blog": "999996789034345"}, 404],
        [999, {"15": "999996789034345"}, 422],
        [0, {"blog": "999996789034345"}, 422],
    ],
)
def test_update_blog_invalid(test_app, monkeypatch, id, payload, status_code):
    async def mock_get(id):
        return None

    monkeypatch.setattr(blog_crud, "get", mock_get)

    response = test_app.put(f"/blog/{id}/", data=json.dumps(payload),)
    assert response.status_code == status_code


# DELETE
def test_remove_blog(test_app, monkeypatch):
    test_data = {"id": 1, "blog": "999996789034345"}

    async def mock_get(id):
        return test_data

    monkeypatch.setattr(blog_crud, "get", mock_get)

    async def mock_delete(id):
        return id

    monkeypatch.setattr(blog_crud, "delete", mock_delete)

    response = test_app.delete("/blog/1/")
    assert response.status_code == 200
    assert response.json() == test_data


def test_remove_blog_incorrect_id(test_app, monkeypatch):
    async def mock_get(id):
        return None

    monkeypatch.setattr(blog_crud, "get", mock_get)

    response = test_app.delete("/blog/999/")
    assert response.status_code == 404
    assert response.json()["Error"] == "blog NOT found"

    response = test_app.delete("/blog/0/")
    assert response.status_code == 422
