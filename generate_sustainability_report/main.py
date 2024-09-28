from contextlib import asynccontextmanager
from fastapi import FastAPI, Depends, HTTPException
from sqlmodel import Session, select
from models import CompanyInfo, CarbonEmissions, WaterUsage, WasteManagement, ESGReports, EmployeeSatisfaction, EnergyConsumption, DiversityInclusion, Products, SupplierCompliance
from database import create_db_and_tables, get_db
from schemas import UserCreate, UserRead, CompanyRead, CompanyCreate, CarbonEmissionsCreate, CompanyInfoCreate
from faker import Faker
from sqlalchemy.exc import SQLAlchemyError
from typing import List
import random
from datetime import datetime
from report_generator import report_generator
from pydantic import BaseModel


class Query(BaseModel):
    query: str


fake = Faker()

INDUSTRIES = [
    "Technology", "Healthcare", "Finance", "Manufacturing", "Retail",
    "Energy", "Telecommunications", "Automotive", "Agriculture", "Education",
    "Entertainment", "Construction", "Transportation", "Hospitality", "Real Estate"
]


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: create database and tables
    create_db_and_tables()
    yield
    # Shutdown: You can add cleanup code here if needed


app = FastAPI(lifespan=lifespan)
query_system = report_generator.SQLQuerySystem(
    db_uri="postgresql://postgres:Hamza@localhost:5432/postgres")


@app.get("/companies/", response_model=List[CompanyInfo])
def read_companies(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    companies = db.exec(select(CompanyInfo).offset(skip).limit(limit)).all()
    return companies


@app.get("/carbon_emissions/", response_model=List[CarbonEmissions])
def read_carbon_emissions(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    emissions = db.exec(
        select(CarbonEmissions).offset(skip).limit(limit)).all()
    return emissions


@app.get("/companies/{company_id}", response_model=CompanyInfo)
def get_company(company_id: int, db: Session = Depends(get_db)):
    company = db.get(CompanyInfo, company_id)
    if not company:
        raise HTTPException(status_code=404, detail="Company not found")
    return company


@app.get("/companies/{company_id}/emissions", response_model=List[CarbonEmissions])
def get_company_emissions(company_id: int, db: Session = Depends(get_db)):
    company = db.get(CompanyInfo, company_id)
    if not company:
        raise HTTPException(status_code=404, detail="Company not found")

    emissions = db.exec(select(CarbonEmissions).where(
        CarbonEmissions.company_id == company_id)).all()
    return emissions


@app.post("/carbon_emissions/", response_model=CarbonEmissions)
def create_carbon_emissions(emissions: CarbonEmissionsCreate, db: Session = Depends(get_db)):
    db_emissions = CarbonEmissions.from_orm(emissions)
    db.add(db_emissions)
    db.commit()
    db.refresh(db_emissions)
    return db_emissions


@app.post("/ingest_random_data/", response_model=dict)
def ingest_random_data(db: Session = Depends(get_db), num_companies: int = 10, years: int = 5):
    try:
        records_created = {
            "CompanyInfo": 0,
            "CarbonEmissions": 0,  # Added CarbonEmissions
            "WaterUsage": 0,
            "WasteManagement": 0,
            "DiversityInclusion": 0,
            "EmployeeSatisfaction": 0,
            "Products": 0,
            "ESGReports": 0,
            "SupplierCompliance": 0
        }

        for _ in range(num_companies):
            # Create a company
            company = CompanyInfo(
                name=fake.company(),
                industry=random.choice(INDUSTRIES),
                employees=fake.random_int(min=100, max=10000),
                year=fake.year()
            )
            db.add(company)
            db.flush()
            records_created["CompanyInfo"] += 1

            # Generate data for multiple years
            for year in range(datetime.now().year - years + 1, datetime.now().year + 1):
                # Carbon Emissions
                carbon_emissions = CarbonEmissions(
                    company_id=company.id,
                    year=year,
                    total_emissions=fake.pyfloat(
                        min_value=1000, max_value=100000),
                    scope_1=fake.pyfloat(min_value=100, max_value=10000),
                    scope_2=fake.pyfloat(min_value=500, max_value=50000),
                    scope_3=fake.pyfloat(min_value=200, max_value=20000)
                )
                db.add(carbon_emissions)
                records_created["CarbonEmissions"] += 1

                # Water Usage
                water_usage = WaterUsage(
                    company_id=company.id,
                    year=year,
                    total_usage=fake.pyfloat(
                        min_value=1000, max_value=1000000),
                    per_capita=fake.pyfloat(min_value=10, max_value=1000),
                    renewable_percentage=fake.pyfloat(
                        min_value=0, max_value=100)
                )
                db.add(water_usage)
                records_created["WaterUsage"] += 1

                # Waste Management
                waste_management = WasteManagement(
                    company_id=company.id,
                    year=year,
                    total_waste=fake.pyfloat(min_value=100, max_value=100000),
                    recycled_percentage=fake.pyfloat(
                        min_value=0, max_value=100),
                    landfill=fake.pyfloat(min_value=10, max_value=50000),
                    recycled=fake.pyfloat(min_value=10, max_value=50000),
                    composted=fake.pyfloat(min_value=0, max_value=10000)
                )
                db.add(waste_management)
                records_created["WasteManagement"] += 1

                # Diversity and Inclusion
                diversity_inclusion = DiversityInclusion(
                    company_id=company.id,
                    year=year,
                    employees=fake.random_int(min=100, max=10000),
                    diversity_percentage=fake.pyfloat(
                        min_value=0, max_value=100),
                    benefits=fake.text(max_nb_chars=200)
                )
                db.add(diversity_inclusion)
                records_created["DiversityInclusion"] += 1

                # Employee Satisfaction
                employee_satisfaction = EmployeeSatisfaction(
                    company_id=company.id,
                    year=year,
                    satisfaction_score=fake.pyfloat(min_value=1, max_value=5),
                    benefits=fake.text(max_nb_chars=200)
                )
                db.add(employee_satisfaction)
                records_created["EmployeeSatisfaction"] += 1

                # Products
                products = Products(
                    company_id=company.id,
                    year=year,
                    products=', '.join(fake.words(nb=3)),
                    benefits=fake.text(max_nb_chars=200)
                )
                db.add(products)
                records_created["Products"] += 1

                # ESG Reports
                esg_report = ESGReports(
                    company_id=company.id,
                    year=year,
                    carbon_emissions_reduction=fake.pyfloat(
                        min_value=0, max_value=50),
                    water_consumption_reduction=fake.pyfloat(
                        min_value=0, max_value=50),
                    generated_at=fake.date_time_this_year().isoformat()
                )
                db.add(esg_report)
                records_created["ESGReports"] += 1

                # Supplier Compliance
                supplier_compliance = SupplierCompliance(
                    company_id=company.id,
                    year=year,
                    compliance_score=fake.pyfloat(min_value=0, max_value=100),
                    sustainable_material_percentage=fake.pyfloat(
                        min_value=0, max_value=100)
                )
                db.add(supplier_compliance)
                records_created["SupplierCompliance"] += 1

        db.commit()
        return {
            "message": "Random data ingested successfully",
            "records_created": records_created
        }

    except Exception as e:
        db.rollback()
        print(f"Error occurred: {str(e)}")
        raise HTTPException(
            status_code=500, detail=f"An error occurred while ingesting data: {str(e)}")

    finally:
        db.close()


@app.post("/energy_consumption/fake_data/", response_model=dict)
def create_fake_energy_consumption(db: Session = Depends(get_db), num_entries: int = 10):
    if num_entries < 1 or num_entries > 10:
        raise HTTPException(
            status_code=400, detail="Number of entries should be between 1 and 10.")

    records_created = []

    for _ in range(num_entries):
        energy_data = EnergyConsumption(
            # Assuming you have company_ids from 1 to 100
            company_id=random.randint(1, 10),
            year=random.randint(2015, 2024),
            total_energy=fake.pyfloat(min_value=1000, max_value=100000),
            electricity=fake.pyfloat(min_value=500, max_value=50000),
            natural_gas=fake.pyfloat(min_value=200, max_value=30000),
            other=fake.pyfloat(min_value=100, max_value=20000),
            renewable_percentage=fake.pyfloat(min_value=0, max_value=100)
        )

        db.add(energy_data)
        db.flush()  # Flush to get the data inserted without committing yet
        db.refresh(energy_data)  # Refresh to get the primary key (id)
        records_created.append(energy_data)

    db.commit()  # Commit once after adding all entries

    return {"message": "Fake EnergyConsumption data created", "records": records_created}


@app.post("/generate-answer", response_model=dict)
def generate_answer(query: Query, db: Session = Depends(get_db)):
    response = query_system.query(query.query)
    return {"response": response}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="localhost", port=8000, reload=True)
