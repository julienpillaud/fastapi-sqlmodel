from typing import Any

from fastapi.testclient import TestClient

from app.entities.pokemons import PokemonCreate


def test_list_pokemons(client: TestClient, inserted_data: list[PokemonCreate]) -> None:
    response = client.get("/pokemons/")
    data = response.json()

    assert response.status_code == 200
    assert len(data) == 2


def test_list_pokemons_by_name(
    client: TestClient, inserted_data: list[PokemonCreate]
) -> None:
    db_pokemon = inserted_data[0]
    response = client.get(f"/pokemons/?name={db_pokemon.name}")
    data = response.json()
    pokemon = data[0]

    assert response.status_code == 200
    assert pokemon["name"] == db_pokemon.name


def test_list_pokemons_by_type(
    client: TestClient, inserted_data: list[PokemonCreate]
) -> None:
    db_pokemon = inserted_data[0]
    response = client.get(f"/pokemons/?pokemon_type={db_pokemon.type1}")
    data = response.json()
    pokemon = data[0]

    assert response.status_code == 200
    assert pokemon["type1"] == db_pokemon.type1


def test_get_pokemon(client: TestClient, inserted_data: list[PokemonCreate]) -> None:
    db_pokemon = inserted_data[0]
    response = client.get(f"/pokemons/{db_pokemon.pokedex_number}")
    data = response.json()

    assert response.status_code == 200
    assert data["pokedex_number"] == db_pokemon.pokedex_number


def test_get_pokemon_not_found(
    client: TestClient, inserted_data: list[PokemonCreate]
) -> None:
    response = client.get("/pokemons/1000")

    assert response.status_code == 404


def test_create_pokemon(client: TestClient, input_data: dict[str, Any]) -> None:
    response = client.post("/pokemons/", json=input_data)
    data = response.json()

    assert response.status_code == 200
    assert data["attack"] == input_data["attack"]
    assert data["classification"] == input_data["classification"]
    assert data["defense"] == input_data["defense"]
    assert data["height_m"] == input_data["height_m"]
    assert data["hp"] == input_data["hp"]
    assert data["japanese_name"] == input_data["japanese_name"]
    assert data["name"] == input_data["name"]
    assert data["sp_attack"] == input_data["sp_attack"]
    assert data["sp_defense"] == input_data["sp_defense"]
    assert data["speed"] == input_data["speed"]
    assert data["type1"] == input_data["type1"]
    assert data["type2"] == input_data["type2"]
    assert data["weight_kg"] == input_data["weight_kg"]
    assert data["generation"] == input_data["generation"]
    assert data["is_legendary"] == input_data["is_legendary"]
    assert data["pokedex_number"] is not None


def test_create_pokemon_incomplete(
    client: TestClient, input_data: dict[str, Any]
) -> None:
    input_data.pop("attack", None)
    response = client.post("/pokemons/", json=input_data)
    assert response.status_code == 422


def test_create_pokemon_invalid(client: TestClient, input_data: dict[str, Any]) -> None:
    input_data["attack"] = "attack"
    response = client.post("/pokemons/", json=input_data)
    assert response.status_code == 422


def test_create_pokemon_already_exists(
    client: TestClient, inserted_data: list[PokemonCreate]
) -> None:
    db_pokemon = inserted_data[0]
    data = db_pokemon.dict()
    response = client.post("/pokemons/", json=data)
    assert response.status_code == 409
