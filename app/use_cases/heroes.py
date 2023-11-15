from app.entities.hero import Hero, HeroCreate, HeroUpdate
from app.use_cases.base import CRUDBase


class CRUDHero(CRUDBase[Hero, HeroCreate, HeroUpdate]):
    pass


hero = CRUDHero(Hero)
