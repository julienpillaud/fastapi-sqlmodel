from typing import Any

from sqlmodel import Session, select

from app.entities.user import User, UserCreate, UserUpdate
from app.security import get_password_hash, verify_password
from app.use_cases.base import CRUDBase


class CRUDUser(CRUDBase[User, UserCreate, UserUpdate]):
    def get_by_email(self, session: Session, email: str) -> User | None:
        return session.exec(select(self.model).where(self.model.email == email)).first()

    def create(self, session: Session, obj_in: UserCreate) -> User:
        db_obj = User(
            email=obj_in.email,
            hashed_password=get_password_hash(obj_in.password),
            is_superuser=obj_in.is_superuser,
        )
        session.add(db_obj)
        session.commit()
        session.refresh(db_obj)
        return db_obj

    def update(
        self, session: Session, db_obj: User, obj_in: UserUpdate | dict[str, Any]
    ) -> User:
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.model_dump(exclude_unset=True)

        if password := update_data.pop("password", None):
            update_data["hashed_password"] = get_password_hash(password)

        return super().update(session, db_obj=db_obj, obj_in=update_data)

    def authenticate(self, session: Session, email: str, password: str) -> User | None:
        user_db = self.get_by_email(session, email=email)
        if not user_db:
            return None
        if not verify_password(password, user_db.hashed_password):
            return None
        return user_db


user = CRUDUser(User)
