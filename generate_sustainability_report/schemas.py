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


class CompanyInfoCreate(SQLModel):
    name: str
    industry: str
    employees: int
    year: int


class CarbonEmissionsCreate(SQLModel):
    company_id: int
    year: int
    total_emissions: float
    scope_1: float
    scope_2: float
    scope_3: float


class CompanyInfoCreate(SQLModel):
    name: str
    industry: str
    employees: int
    year: int
