from fastapi.testclient import TestClient
from sqlmodel import Session

from app.entities.user import User
from app.security import get_password_hash


def fetch_authentication_headers(
    client: TestClient, email: str, password: str
) -> dict[str, str]:
    input_data = {"username": email, "password": password}
    response = client.post("/token", data=input_data)
    data = response.json()
    auth_token = data["access_token"]
    headers = {"Authorization": f"Bearer {auth_token}"}
    return headers


def get_authentication_headers(
    session: Session, client: TestClient, is_superuser: bool = False
) -> dict[str, str]:
    email = "test@test.com"
    password = "test"
    user = User(
        email=email,
        hashed_password=get_password_hash(password),
        is_superuser=is_superuser,
    )
    session.add(user)
    session.commit()
    return fetch_authentication_headers(client=client, email=email, password=password)
