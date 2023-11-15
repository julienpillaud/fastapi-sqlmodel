from typing import Any

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlmodel import Session

from app import use_cases
from app.dependencies import get_session
from app.entities.common import HeroReadWithTeam
from app.entities.hero import HeroCreate, HeroRead, HeroUpdate

router = APIRouter(prefix="/heroes", tags=["heroes"])


@router.post("/", response_model=HeroRead)
def create_hero(*, session: Session = Depends(get_session), hero: HeroCreate) -> Any:
    return use_cases.hero.create(session=session, obj_in=hero)


@router.get("/", response_model=list[HeroRead])
def read_heroes(
    *,
    session: Session = Depends(get_session),
    offset: int = 0,
    limit: int = Query(default=100, le=100),
) -> Any:
    return use_cases.hero.get_multi(session=session, offset=offset, limit=limit)


@router.get("/{hero_id}", response_model=HeroReadWithTeam)
def read_hero(*, session: Session = Depends(get_session), hero_id: int) -> Any:
    hero_db = use_cases.hero.get(session=session, obj_id=hero_id)
    if not hero_db:
        raise HTTPException(status_code=404, detail="Hero not found")
    return hero_db


@router.patch("/{hero_id}", response_model=HeroRead)
def update_hero(
    *, session: Session = Depends(get_session), hero_id: int, hero: HeroUpdate
) -> Any:
    hero_db = use_cases.hero.get(session=session, obj_id=hero_id)
    if not hero_db:
        raise HTTPException(status_code=404, detail="Hero not found")
    return use_cases.hero.update(session=session, db_obj=hero_db, obj_in=hero)


@router.delete("/{hero_id}")
def delete_hero(*, session: Session = Depends(get_session), hero_id: int) -> Any:
    hero_db = use_cases.hero.get(session=session, obj_id=hero_id)
    if not hero_db:
        raise HTTPException(status_code=404, detail="Hero not found")
    use_cases.hero.remove(session=session, db_obj=hero_db)
