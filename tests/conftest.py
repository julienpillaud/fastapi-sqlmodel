from collections.abc import Iterator
from typing import Any

import pytest
from fastapi.testclient import TestClient
from sqlmodel import Session, SQLModel, create_engine
from sqlmodel.pool import StaticPool

from app.dependencies import get_session
from app.entities.pokemons import Pokemon, PokemonCreate
from app.main import app
from scripts.pokemons import pokemons

pokemons_to_insert = [PokemonCreate.parse_obj(pokemon) for pokemon in pokemons[:2]]


@pytest.fixture(name="session")
def session_fixture() -> Iterator[Session]:
    engine = create_engine(
        "sqlite://", connect_args={"check_same_thread": False}, poolclass=StaticPool
    )
    SQLModel.metadata.create_all(engine)
    with Session(engine) as session:
        yield session


@pytest.fixture(name="client")
def client_fixture(session: Session) -> Iterator[TestClient]:
    def get_session_override() -> Session:
        return session

    app.dependency_overrides[get_session] = get_session_override

    client = TestClient(app)
    yield client
    app.dependency_overrides.clear()


@pytest.fixture(name="input_data")
def pokemon_data_fixture() -> dict[str, Any]:
    return pokemons[0]


@pytest.fixture(name="inserted_data")
def populate_database(session: Session) -> list[PokemonCreate]:
    session.bulk_save_objects(
        [Pokemon.from_orm(pokemon) for pokemon in pokemons_to_insert]
    )
    session.commit()
    return pokemons_to_insert
