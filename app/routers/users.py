from typing import Annotated, Any

from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session

from app import use_cases
from app.dependencies import get_current_active_superuser, get_current_user, get_session
from app.entities.user import User, UserCreate, UserRead, UserUpdate

router = APIRouter(prefix="/users", tags=["users"])


@router.post("/", response_model=UserRead)
def create_user(
    *,
    session: Annotated[Session, Depends(get_session)],
    user_in: UserCreate,
) -> Any:
    user = use_cases.user.get_by_email(session, email=user_in.email)
    if user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="The user with this username already exists.",
        )
    return use_cases.user.create(session, obj_in=user_in)


@router.get("/", response_model=list[UserRead])
def read_users(
    *,
    session: Annotated[Session, Depends(get_session)],
    offset: int = 0,
    limit: int = 100,
    current_user: Annotated[User, Depends(get_current_active_superuser)],
) -> Any:
    return use_cases.user.get_multi(session, offset=offset, limit=limit)


@router.get("/me", response_model=UserRead)
def read_user_me(
    current_user: Annotated[User, Depends(get_current_user)],
) -> Any:
    return current_user


@router.put("/me", response_model=UserRead)
def update_user_me(
    *,
    session: Session = Depends(get_session),
    user_in: UserUpdate,
    current_user: User = Depends(get_current_user),
) -> Any:
    return use_cases.user.update(session, db_obj=current_user, obj_in=user_in)


@router.put("/{user_id}", response_model=UserRead)
def update_user(
    *,
    session: Session = Depends(get_session),
    user_id: int,
    user_in: UserUpdate,
    current_user: User = Depends(get_current_active_superuser),
) -> Any:
    user = use_cases.user.get(session, obj_id=user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="The user with this username does not exist",
        )
    return use_cases.user.update(session, db_obj=user, obj_in=user_in)
