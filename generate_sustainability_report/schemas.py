from sqlmodel import SQLModel


class UserCreate(SQLModel):
    name: str
    email: str


class UserRead(SQLModel):
    id: int
    name: str
    email: str


class CompanyRead(SQLModel):
    id: int
    company_name: str
    industry: str
    country: str


class CompanyCreate(SQLModel):
    company_name: str
    industry: str
    country: str
