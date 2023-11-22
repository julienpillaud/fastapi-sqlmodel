from fastapi import status
from fastapi.testclient import TestClient
from sqlmodel import Session

from app.entities.user import User
from app.security import get_password_hash


def test_create_user(client: TestClient, normal_user_headers: dict[str, str]) -> None:
    json_data = {"email": "user@test.com", "password": "user"}
    response = client.post("users/", headers=normal_user_headers, json=json_data)
    data = response.json()

    assert response.status_code == status.HTTP_200_OK
    assert data["email"] == json_data["email"]
    assert data["is_superuser"] is False
    assert data["id"] is not None


def test_create_user_incomplete(
    client: TestClient, normal_user_headers: dict[str, str]
) -> None:
    # No password
    json_data = {"email": "user@test.com"}
    response = client.post("users/", headers=normal_user_headers, json=json_data)
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


def test_create_user_invalid(
    client: TestClient, normal_user_headers: dict[str, str]
) -> None:
    # password has an invalid type
    json_data = {"email": "user@test.com", "password": {"bad": "user"}}
    response = client.post("users/", headers=normal_user_headers, json=json_data)
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY


def test_read_users(client: TestClient, superuser_headers: dict[str, str]) -> None:
    response = client.get("/users", headers=superuser_headers)
    data = response.json()

    assert response.status_code == status.HTTP_200_OK
    assert data
    assert data[0]["email"] == "test@test.com"
    assert data[0]["is_superuser"] is True
    assert data[0]["id"] is not None


def test_read_user_me(client: TestClient, normal_user_headers: dict[str, str]) -> None:
    response = client.get("/users/me", headers=normal_user_headers)
    data = response.json()

    assert response.status_code == status.HTTP_200_OK
    assert data["email"] == "test@test.com"
    assert data["is_superuser"] is False
    assert data["id"] is not None


def test_update_user(
    session: Session, client: TestClient, superuser_headers: dict[str, str]
) -> None:
    user = User(
        email="user@test.com",
        hashed_password=get_password_hash("test"),
    )
    session.add(user)
    session.commit()

    json_data = {"password": "new password"}
    response = client.put(
        f"/users/{user.id}", headers=superuser_headers, json=json_data
    )
    data = response.json()

    assert response.status_code == 200
    assert data["email"] == "user@test.com"
    assert data["is_superuser"] is False
    assert data["id"] == user.id


def test_update_user_me(
    session: Session, client: TestClient, normal_user_headers: dict[str, str]
) -> None:
    json_data = {"password": "new password"}
    response = client.put("/users/me", headers=normal_user_headers, json=json_data)
    data = response.json()

    assert response.status_code == 200
    assert data["email"] == "test@test.com"
    assert data["is_superuser"] is False
