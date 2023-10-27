from typing import Generic, Type, TypeVar

from sqlmodel import Session, SQLModel

SchemaType = TypeVar("SchemaType", bound=SQLModel)
CreateSchemaType = TypeVar("CreateSchemaType", bound=SQLModel)


class CRUDBase(Generic[SchemaType, CreateSchemaType]):
    def __init__(self, model: Type[SchemaType]):
        self.model = model

    def get(self, session: Session, obj_id: int) -> SchemaType | None:
        return session.get(self.model, obj_id)

    def create(self, session: Session, obj_in: CreateSchemaType) -> SchemaType:
        db_obj = self.model.from_orm(obj_in)
        session.add(db_obj)
        session.commit()
        session.refresh(db_obj)
        return db_obj
