from sqlmodel import Session, select

from app.entities.pokemons import Pokemon, PokemonCreate, PokemonType
from app.use_cases.base import CRUDBase


class CRUDPokemon(CRUDBase[Pokemon, PokemonCreate]):
    def get_by_filter(
        self,
        session: Session,
        name: str | None = None,
        pokemon_type: PokemonType | None = None,
    ) -> list[Pokemon]:
        statement = select(self.model)
        if name:
            statement = statement.where(Pokemon.name == name)
        if pokemon_type:
            statement = statement.where(Pokemon.type1 == pokemon_type)
        return session.exec(statement).all()

    def get_by_pokedex_number(
        self, session: Session, pokedex_number: int
    ) -> Pokemon | None:
        return session.exec(
            select(self.model).where(Pokemon.pokedex_number == pokedex_number)
        ).first()


pokemon = CRUDPokemon(Pokemon)
