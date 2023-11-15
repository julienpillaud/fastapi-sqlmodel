from app.entities.team import Team, TeamCreate, TeamUpdate
from app.use_cases.base import CRUDBase


class CRUDTeam(CRUDBase[Team, TeamCreate, TeamUpdate]):
    pass


team = CRUDTeam(Team)
