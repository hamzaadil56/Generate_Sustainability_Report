from contextlib import asynccontextmanager
from fastapi import FastAPI, Depends, HTTPException
from sqlmodel import Session, select
from models import CompanyInfo, CarbonEmissions
from database import create_db_and_tables, get_db
from schemas import UserCreate, UserRead, CompanyRead, CompanyCreate, CarbonEmissionsCreate, CompanyInfoCreate
from faker import Faker
from sqlalchemy.exc import SQLAlchemyError
from typing import List
import random

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


@app.post("/ingest_data/")
def ingest_data(db: Session = Depends(get_db)):
    companies_created: List[int] = []
    emissions_created: List[int] = []

    try:
        for _ in range(10):  # Create 10 sample companies
            company = CompanyInfo(
                name=fake.company(),
                industry=random.choice(INDUSTRIES),
                employees=fake.random_int(min=100, max=10000),
                year=fake.year()
            )
            db.add(company)
            db.flush()  # Flush to get the ID without committing
            companies_created.append(company.id)

            # Create carbon emissions data for each company
            emissions = CarbonEmissions(
                company_id=company.id,
                year=company.year,
                total_emissions=fake.pyfloat(min_value=1000, max_value=100000),
                scope_1=fake.pyfloat(min_value=100, max_value=10000),
                scope_2=fake.pyfloat(min_value=500, max_value=50000),
                scope_3=fake.pyfloat(min_value=200, max_value=20000)
            )
            db.add(emissions)
            db.flush()
            emissions_created.append(emissions.id)

        # If everything is successful, commit the transaction
        db.commit()
        return {
            "message": "Sample data ingested successfully",
            "companies_created": len(companies_created),
            "emissions_records_created": len(emissions_created)
        }

    except SQLAlchemyError as e:
        # If there's an error, roll back the transaction
        db.rollback()
        # Log the error (you should set up proper logging)
        print(f"Database error occurred: {str(e)}")
        raise HTTPException(
            status_code=500, detail="An error occurred while ingesting data")

    except Exception as e:
        # Catch any other unexpected errors
        db.rollback()
        print(f"Unexpected error occurred: {str(e)}")
        raise HTTPException(
            status_code=500, detail="An unexpected error occurred")

    finally:
        # Close the database session
        db.close()


# @app.post("/users/", response_model=UserRead)
# def create_user(user: UserCreate, db: Session = Depends(get_db)):
#     statement = select(User).where(User.email == user.email)
#     existing_user = db.exec(statement).first()
#     if existing_user:
#         raise HTTPException(status_code=400, detail="Email already registered")

#     new_user = User(name=user.name, email=user.email)
#     db.add(new_user)
#     db.commit()
#     db.refresh(new_user)
#     return new_user


# @app.get("/users/{user_id}", response_model=UserRead)
# def read_user(user_id: int, db: Session = Depends(get_db)):
#     user = db.get(User, user_id)
#     if not user:
#         raise HTTPException(status_code=404, detail="User not found")
#     return user


# @app.get("/companies/", response_model=list[CompanyRead])
# def get_all_companies(db: Session = Depends(get_db)):
#     companies = db.exec(select(Companies)).all()
#     return companies


# @app.get("/companies/{company_id}", response_model=CompanyRead)
# def get_company(company_id: int, db: Session = Depends(get_db)):
#     company = db.get(Companies, company_id)
#     if not company:
#         raise HTTPException(status_code=404, detail="Company not found")
#     return company


# @app.post("/companies/", response_model=CompanyRead)
# def create_company(company: CompanyCreate, db: Session = Depends(get_db)):
#     new_company = Companies(
#         company_name=company.company_name,
#         industry=company.industry,
#         country=company.country
#     )
#     db.add(new_company)
#     db.commit()
#     db.refresh(new_company)
#     return new_company


# @app.post("/companies/random", response_model=list[CompanyRead])
# def create_random_companies(db: Session = Depends(get_db), count: int = 100):
#     new_companies = []

#     for _ in range(count):
#         company_data = CompanyCreate(
#             company_name=fake.company(),
#             industry=fake.bs(),
#             country=fake.country()
#         )
#         new_company = Companies(
#             company_name=company_data.company_name,
#             industry=company_data.industry,
#             country=company_data.country
#         )
#         db.add(new_company)
#         new_companies.append(new_company)

#     db.commit()
#     for company in new_companies:
#         db.refresh(company)
#     return new_companies
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="localhost", port=8000, reload=True)
