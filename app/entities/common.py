from app.entities.hero import HeroRead
from app.entities.team import TeamRead


class HeroReadWithTeam(HeroRead):
    team: TeamRead | None = None


class TeamReadWithHeroes(TeamRead):
    heroes: list[HeroRead] = []
