from sqlmodel import SQLModel, Field
from typing import Optional


class CompanyInfo(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    name: str
    industry: str
    employees: int
    year: int


# class CarbonEmissions(SQLModel, table=True):
#     id: int = Field(default=None, primary_key=True)
#     company_id: int = Field(foreign_key="companyinfo.id")
#     year: int
#     total_emissions: float
#     scope_1: float
#     scope_2: float
#     scope_3: float


# class Companies(SQLModel, table=True):
#     id: int = Field(default=None, primary_key=True)
#     company_name: str
#     industry: str
#     country: str


class CarbonEmissions(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    company_id: int = Field(foreign_key="companyinfo.id")
    year: int
    total_emissions: float
    scope_1: float
    scope_2: float
    scope_3: float
