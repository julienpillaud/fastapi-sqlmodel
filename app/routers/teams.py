from typing import Any

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlmodel import Session

from app import use_cases
from app.dependencies import get_session
from app.entities.common import TeamReadWithHeroes
from app.entities.team import TeamCreate, TeamRead, TeamUpdate

router = APIRouter(prefix="/teams", tags=["teams"])


@router.post("/", response_model=TeamRead)
def create_team(*, session: Session = Depends(get_session), team: TeamCreate) -> Any:
    return use_cases.team.create(session=session, obj_in=team)


@router.get("/", response_model=list[TeamRead])
def read_teams(
    *,
    session: Session = Depends(get_session),
    offset: int = 0,
    limit: int = Query(default=100, le=100),
) -> Any:
    return use_cases.team.get_multi(session=session, offset=offset, limit=limit)


@router.get("/{team_id}", response_model=TeamReadWithHeroes)
def read_team(*, team_id: int, session: Session = Depends(get_session)) -> Any:
    team_db = use_cases.team.get(session=session, obj_id=team_id)
    if not team_db:
        raise HTTPException(status_code=404, detail="Team not found")
    return team_db


@router.patch("/{team_id}", response_model=TeamRead)
def update_team(
    *,
    session: Session = Depends(get_session),
    team_id: int,
    team: TeamUpdate,
) -> Any:
    team_db = use_cases.team.get(session=session, obj_id=team_id)
    if not team_db:
        raise HTTPException(status_code=404, detail="Team not found")
    return use_cases.team.update(session=session, db_obj=team_db, obj_in=team)


@router.delete("/{team_id}")
def delete_team(*, session: Session = Depends(get_session), team_id: int) -> Any:
    team_db = use_cases.team.get(session=session, obj_id=team_id)
    if not team_db:
        raise HTTPException(status_code=404, detail="Team not found")
    use_cases.team.remove(session=session, db_obj=team_db)
