from typing import Any

import httpx

from scripts.pokemons import pokemons

url = "http://127.0.0.1:8000/pokemons/"


def create_pokemons(data: dict[str, Any]) -> httpx.Response:
    return httpx.post(url, json=data)


if __name__ == "__main__":
    for pokemon in pokemons:
        response = create_pokemons(data=pokemon)
        print(response.json())
