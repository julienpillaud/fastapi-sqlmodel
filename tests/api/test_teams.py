from sqlmodel import Session
from starlette.testclient import TestClient

from app.entities.hero import Hero
from app.entities.team import Team


def test_create_team(client: TestClient) -> None:
    json_data = {"name": "Preventers", "headquarters": "Sharp Tower"}
    response = client.post("/teams/", json=json_data)
    data = response.json()

    assert response.status_code == 200
    assert data["name"] == json_data["name"]
    assert data["headquarters"] == json_data["headquarters"]
    assert data["id"] is not None


def test_create_team_incomplete(client: TestClient) -> None:
    # No headquarters
    response = client.post("/heroes/", json={"name": "Preventers"})
    assert response.status_code == 422


def test_create_team_invalid(client: TestClient) -> None:
    # headquarters has an invalid type
    response = client.post(
        "/heroes/",
        json={
            "name": "Preventers",
            "headquarters": {"message": "Error"},
        },
    )
    assert response.status_code == 422


def test_read_teams(session: Session, client: TestClient) -> None:
    hero_1 = Hero(name="Deadpond", secret_name="Dive Wilson")
    hero_2 = Hero(name="Rusty-Man", secret_name="Tommy Sharp", age=48)
    team_1 = Team(
        name="Preventers", headquarters="Sharp Tower", heroes=[hero_1, hero_2]
    )
    team_2 = Team(name="Z-Force", headquarters="Sister Margaret’s Bar")
    session.add(team_1)
    session.add(team_2)
    session.commit()

    response = client.get("/teams/")
    data = response.json()

    assert response.status_code == 200

    assert len(data) == 2
    assert data[0]["name"] == team_1.name
    assert data[0]["headquarters"] == team_1.headquarters
    assert data[0]["id"] == team_1.id
    assert data[0].get("heroes") is None

    assert data[1]["name"] == team_2.name
    assert data[1]["headquarters"] == team_2.headquarters
    assert data[1]["id"] == team_2.id
    assert data[1].get("heroes") is None


def test_read_team(session: Session, client: TestClient) -> None:
    hero_1 = Hero(name="Deadpond", secret_name="Dive Wilson")
    hero_2 = Hero(name="Rusty-Man", secret_name="Tommy Sharp", age=48)
    team_1 = Team(
        name="Preventers", headquarters="Sharp Tower", heroes=[hero_1, hero_2]
    )
    session.add(team_1)
    session.commit()

    response = client.get(f"/teams/{team_1.id}")
    data = response.json()

    assert response.status_code == 200
    assert data["name"] == team_1.name
    assert data["headquarters"] == team_1.headquarters
    assert data["id"] == team_1.id

    assert data["heroes"][0]["name"] == hero_1.name
    assert data["heroes"][0]["secret_name"] == hero_1.secret_name
    assert data["heroes"][0]["age"] is None
    assert data["heroes"][0]["id"] == hero_1.id

    assert data["heroes"][1]["name"] == hero_2.name
    assert data["heroes"][1]["secret_name"] == hero_2.secret_name
    assert data["heroes"][1]["age"] == hero_2.age
    assert data["heroes"][1]["id"] == hero_2.id


def test_update_team(session: Session, client: TestClient) -> None:
    team_1 = Team(name="Preventers", headquarters="Sharp Tower")
    session.add(team_1)
    session.commit()

    json_data = {"name": "Preventlle"}
    response = client.patch(f"/teams/{team_1.id}", json=json_data)
    data = response.json()

    assert response.status_code == 200
    assert data["name"] == json_data["name"]
    assert data["headquarters"] == team_1.headquarters
    assert data["id"] == team_1.id


def test_delete_team(session: Session, client: TestClient) -> None:
    team_1 = Team(name="Preventers", headquarters="Sharp Tower")
    session.add(team_1)
    session.commit()

    response = client.delete(f"/teams/{team_1.id}")

    team_in_db = session.get(Team, team_1.id)

    assert response.status_code == 200

    assert team_in_db is None
