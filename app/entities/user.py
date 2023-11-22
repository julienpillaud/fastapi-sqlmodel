from sqlmodel import Field, SQLModel


class User(SQLModel, table=True):
    id: int | None = Field(default=None, primary_key=True)
    email: str = Field(unique=True)
    hashed_password: str
    is_superuser: bool = Field(default=False)


class UserCreate(SQLModel):
    email: str
    password: str
    is_superuser: bool = False


class UserUpdate(SQLModel):
    password: str


class UserRead(SQLModel):
    id: int
    email: str
    is_superuser: bool
