from datetime import timedelta
from typing import Annotated, Any

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlmodel import Session

from app import use_cases
from app.config import settings
from app.dependencies import get_session
from app.entities.token import Token
from app.security import create_access_token

router = APIRouter(tags=["login"])


@router.post("/token", response_model=Token)
def login_for_access_token(
    *,
    session: Session = Depends(get_session),
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
) -> Any:
    user = use_cases.user.authenticate(
        session, email=form_data.username, password=form_data.password
    )
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
        )
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(data=user.id, expires_delta=access_token_expires)
    return {"access_token": access_token, "token_type": "bearer"}
