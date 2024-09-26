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


class EnergyConsumption(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    company_id: int = Field(foreign_key="companyinfo.id")
    year: int
    total_energy: float
    electricity: float
    natural_gas: float
    other: float
    renewable_percentage: float


class WaterUsage(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    company_id: int = Field(foreign_key="companyinfo.id")
    year: int
    total_usage: float
    per_capita: float
    renewable_percentage: float


class WasteManagement(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    company_id: int = Field(foreign_key="companyinfo.id")
    year: int
    total_waste: float
    recycled_percentage: float
    landfill: float
    recycled: float
    composted: float


class DiversityInclusion(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    company_id: int = Field(foreign_key="companyinfo.id")
    year: int
    employees: int
    diversity_percentage: float
    benefits: Optional[str] = None


class EmployeeSatisfaction(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    company_id: int = Field(foreign_key="companyinfo.id")
    year: int
    satisfaction_score: float
    benefits: Optional[str] = None


class Products(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    company_id: int = Field(foreign_key="companyinfo.id")
    year: int
    products: str
    benefits: Optional[str] = None


class ESGReports(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    company_id: int = Field(foreign_key="companyinfo.id")
    year: int
    carbon_emissions_reduction: float
    water_consumption_reduction: float
    generated_at: str


class SupplierCompliance(SQLModel, table=True):
    id: int = Field(default=None, primary_key=True)
    company_id: int = Field(foreign_key="companyinfo.id")
    year: int
    compliance_score: float
    sustainable_material_percentage: float
