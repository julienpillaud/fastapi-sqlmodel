from typing import Any, Generic, Sequence, Type, TypeVar

from fastapi.encoders import jsonable_encoder
from sqlmodel import Session, SQLModel, select

SchemaType = TypeVar("SchemaType", bound=SQLModel)
CreateSchemaType = TypeVar("CreateSchemaType", bound=SQLModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=SQLModel)


class CRUDBase(Generic[SchemaType, CreateSchemaType, UpdateSchemaType]):
    def __init__(self, model: Type[SchemaType]):
        self.model = model

    def create(self, session: Session, obj_in: CreateSchemaType) -> SchemaType:
        db_obj = self.model.model_validate(obj_in)
        session.add(db_obj)
        session.commit()
        session.refresh(db_obj)
        return db_obj

    def get(self, session: Session, obj_id: int) -> SchemaType | None:
        return session.get(self.model, obj_id)

    def get_multi(
        self, session: Session, offset: int = 0, limit: int = 0
    ) -> Sequence[SchemaType]:
        return session.exec(select(self.model).offset(offset).limit(limit)).all()

    def update(
        self,
        session: Session,
        db_obj: SchemaType,
        obj_in: UpdateSchemaType | dict[str, Any],
    ) -> SchemaType:
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.model_dump(exclude_unset=True)

        for field in jsonable_encoder(db_obj):
            if field in update_data:
                setattr(db_obj, field, update_data[field])

        session.add(db_obj)
        session.commit()
        session.refresh(db_obj)
        return db_obj

    @staticmethod
    def remove(session: Session, db_obj: SchemaType) -> None:
        session.delete(db_obj)
        session.commit()
