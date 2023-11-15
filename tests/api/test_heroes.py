from fastapi.testclient import TestClient
from sqlmodel import Session

from app.entities.hero import Hero
from app.entities.team import Team


def test_create_hero(client: TestClient) -> None:
    json_data = {"name": "Deadpond", "secret_name": "Dive Wilson"}
    response = client.post("/heroes/", json=json_data)
    data = response.json()

    assert response.status_code == 200
    assert data["name"] == json_data["name"]
    assert data["secret_name"] == json_data["secret_name"]
    assert data["age"] is None
    assert data["id"] is not None


def test_create_hero_incomplete(client: TestClient) -> None:
    # No secret_name
    response = client.post("/heroes/", json={"name": "Deadpond"})
    assert response.status_code == 422


def test_create_hero_invalid(client: TestClient) -> None:
    # secret_name has an invalid type
    response = client.post(
        "/heroes/",
        json={
            "name": "Deadpond",
            "secret_name": {"message": "Do you wanna know my secret identity?"},
        },
    )
    assert response.status_code == 422


def test_read_heroes(session: Session, client: TestClient) -> None:
    team_1 = Team(name="Preventers", headquarters="Sharp Tower")
    team_2 = Team(name="Z-Force", headquarters="Sister Margaret’s Bar")
    hero_1 = Hero(name="Deadpond", secret_name="Dive Wilson", team=team_1)
    hero_2 = Hero(name="Rusty-Man", secret_name="Tommy Sharp", age=48, team=team_2)
    hero_3 = Hero(name="Spider-Boy", secret_name="Pedro Parqueador")
    session.add(hero_1)
    session.add(hero_2)
    session.add(hero_3)
    session.commit()

    response = client.get("/heroes/")
    data = response.json()

    assert response.status_code == 200

    assert len(data) == 3
    assert data[0]["name"] == hero_1.name
    assert data[0]["secret_name"] == hero_1.secret_name
    assert data[0]["age"] == hero_1.age
    assert data[0]["id"] == hero_1.id
    assert data[0]["team_id"] == team_1.id
    assert data[0].get("team") is None

    assert data[1]["name"] == hero_2.name
    assert data[1]["secret_name"] == hero_2.secret_name
    assert data[1]["age"] == hero_2.age
    assert data[1]["id"] == hero_2.id
    assert data[1]["team_id"] == team_2.id
    assert data[1].get("team") is None

    assert data[2]["name"] == hero_3.name
    assert data[2]["secret_name"] == hero_3.secret_name
    assert data[2]["age"] == hero_3.age
    assert data[2]["id"] == hero_3.id
    assert data[2]["team_id"] is None
    assert data[2].get("team") is None


def test_read_hero(session: Session, client: TestClient) -> None:
    team_1 = Team(name="Preventers", headquarters="Sharp Tower")
    hero_1 = Hero(name="Deadpond", secret_name="Dive Wilson", team=team_1)
    session.add(hero_1)
    session.commit()

    response = client.get(f"/heroes/{hero_1.id}")
    data = response.json()

    assert response.status_code == 200
    assert data["name"] == hero_1.name
    assert data["secret_name"] == hero_1.secret_name
    assert data["age"] == hero_1.age
    assert data["id"] == hero_1.id
    assert data["team_id"] == team_1.id

    assert data["team"]["name"] == team_1.name
    assert data["team"]["headquarters"] == team_1.headquarters
    assert data["team"]["id"] == team_1.id


def test_update_hero(session: Session, client: TestClient) -> None:
    hero_1 = Hero(name="Deadpond", secret_name="Dive Wilson")
    session.add(hero_1)
    session.commit()

    json_data = {"name": "Deadpuddle"}
    response = client.patch(f"/heroes/{hero_1.id}", json=json_data)
    data = response.json()

    assert response.status_code == 200
    assert data["name"] == json_data["name"]
    assert data["secret_name"] == hero_1.secret_name
    assert data["age"] == hero_1.age
    assert data["id"] == hero_1.id


def test_delete_hero(session: Session, client: TestClient) -> None:
    hero_1 = Hero(name="Deadpond", secret_name="Dive Wilson")
    session.add(hero_1)
    session.commit()

    response = client.delete(f"/heroes/{hero_1.id}")

    hero_in_db = session.get(Hero, hero_1.id)

    assert response.status_code == 200

    assert hero_in_db is None
