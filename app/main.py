from collections.abc import AsyncIterator
from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.database import create_db_and_tables
from app.routers import pokemons


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterator[None]:  # noqa
    create_db_and_tables()
    yield


app = FastAPI(lifespan=lifespan)

app.include_router(pokemons.router)