from collections.abc import Iterator
from typing import Annotated

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from pydantic import ValidationError
from sqlmodel import Session

from app import use_cases
from app.config import settings
from app.database import engine
from app.entities.token import TokenData
from app.entities.user import User
from app.security import ALGORITHM

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


def get_session() -> Iterator[Session]:
    with Session(engine) as session:
        yield session


def get_current_user(
    session: Annotated[Session, Depends(get_session)],
    token: Annotated[str, Depends(oauth2_scheme)],
) -> User:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
    )

    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[ALGORITHM])
        token_data = TokenData.model_validate(payload)
    except (JWTError, ValidationError):
        raise credentials_exception from JWTError

    user = use_cases.user.get(session, obj_id=int(token_data.sub))
    if not user:
        raise credentials_exception
    return user


def get_current_active_superuser(
    current_user: Annotated[User, Depends(get_current_user)],
) -> User:
    if not current_user.is_superuser:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="The user doesn't have enough privileges",
        )
    return current_user
