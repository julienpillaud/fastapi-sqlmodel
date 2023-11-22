from collections.abc import Iterator

import pytest
from fastapi.testclient import TestClient
from sqlmodel import Session, SQLModel, create_engine
from sqlmodel.pool import StaticPool

from app.dependencies import get_session
from app.main import app
from tests.utils.users import get_authentication_headers


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


@pytest.fixture
def superuser_headers(session: Session, client: TestClient) -> dict[str, str]:
    return get_authentication_headers(session=session, client=client, is_superuser=True)


@pytest.fixture
def normal_user_headers(session: Session, client: TestClient) -> dict[str, str]:
    return get_authentication_headers(session=session, client=client)
