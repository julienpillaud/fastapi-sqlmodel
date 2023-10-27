from typing import Any

from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session

from app import use_cases
from app.dependencies import get_session
from app.entities.pokemons import PokemonCreate, PokemonRead, PokemonType

router = APIRouter(prefix="/pokemons", tags=["pokemons"])


@router.get("/", response_model=list[PokemonRead])
def list_pokemons(
    *,
    session: Session = Depends(get_session),
    name: str | None = None,
    pokemon_type: PokemonType | None = None
) -> Any:
    return use_cases.pokemon.get_by_filter(
        session=session, name=name, pokemon_type=pokemon_type
    )


@router.get("/{pokedex_number}", response_model=PokemonRead)
def get_pokemon(*, session: Session = Depends(get_session), pokedex_number: int) -> Any:
    pokemon = use_cases.pokemon.get_by_pokedex_number(
        session=session, pokedex_number=pokedex_number
    )
    if not pokemon:
        raise HTTPException(status_code=404, detail="Pokemon not found")
    return pokemon


@router.post("/", response_model=PokemonRead)
def create_pokemon(
    *, session: Session = Depends(get_session), pokemon_in: PokemonCreate
) -> Any:
    pokemon = use_cases.pokemon.get_by_pokedex_number(
        session=session, pokedex_number=pokemon_in.pokedex_number
    )
    if pokemon:
        raise HTTPException(status_code=409, detail="Pokemon already exists")
    return use_cases.pokemon.create(session=session, obj_in=pokemon_in)
