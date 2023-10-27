from enum import StrEnum

from sqlmodel import Field, SQLModel


class PokemonType(StrEnum):
    BUG = "bug"
    DARK = "dark"
    DRAGON = "dragon"
    ELECTRIC = "electric"
    FAIRY = "fairy"
    FIGHTING = "fighting"
    FIRE = "fire"
    FLYING = "flying"
    GHOST = "ghost"
    GRASS = "grass"
    GROUND = "ground"
    ICE = "ice"
    NORMAL = "normal"
    POISON = "poison"
    PSYCHIC = "psychic"
    ROCK = "rock"
    STEEL = "steel"
    WATER = "water"


class PokemonBase(SQLModel):
    attack: int
    classification: str
    defense: int
    height_m: float | None
    hp: int
    japanese_name: str
    name: str = Field(index=True)
    pokedex_number: int = Field(index=True, unique=True)
    sp_attack: int
    sp_defense: int
    speed: int
    type1: PokemonType = Field(index=True)
    type2: PokemonType | None
    weight_kg: float | None
    generation: int
    is_legendary: bool


class Pokemon(PokemonBase, table=True):
    id: int | None = Field(default=None, primary_key=True)


class PokemonCreate(PokemonBase):
    pass


class PokemonRead(PokemonBase):
    pokedex_number: int
