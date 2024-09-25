from sqlmodel import SQLModel, Field
from typing import Optional


class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    email: str = Field(index=True, unique=True)


class Companies(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    company_name: str
    industry: str
    country: str
