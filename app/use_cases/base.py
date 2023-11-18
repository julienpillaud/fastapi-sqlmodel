from typing import Generic, Sequence, Type, TypeVar

from sqlmodel import Session, SQLModel, select

SchemaType = TypeVar("SchemaType", bound=SQLModel)
CreateSchemaType = TypeVar("CreateSchemaType", bound=SQLModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=SQLModel)


class CRUDBase(Generic[SchemaType, CreateSchemaType, UpdateSchemaType]):
    def __init__(self, model: Type[SchemaType]):
        self.model = model

    def create(self, session: Session, obj_in: CreateSchemaType) -> SchemaType:
        db_obj = self.model.from_orm(obj_in)
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

    @staticmethod
    def update(
        session: Session, db_obj: SchemaType, obj_in: UpdateSchemaType
    ) -> SchemaType:
        obj_data = obj_in.dict(exclude_unset=True)
        for key, value in obj_data.items():
            setattr(db_obj, key, value)
        session.add(db_obj)
        session.commit()
        session.refresh(db_obj)
        return db_obj

    @staticmethod
    def remove(session: Session, db_obj: SchemaType) -> None:
        session.delete(db_obj)
        session.commit()
