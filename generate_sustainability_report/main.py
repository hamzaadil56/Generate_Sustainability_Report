from contextlib import asynccontextmanager
from fastapi import FastAPI, Depends, HTTPException
from sqlmodel import Session, select
from models import User, Companies
from database import create_db_and_tables, get_db
from schemas import UserCreate, UserRead, CompanyRead, CompanyCreate
from faker import Faker

fake = Faker()


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: create database and tables
    create_db_and_tables()
    yield
    # Shutdown: You can add cleanup code here if needed

app = FastAPI(lifespan=lifespan)


@app.post("/users/", response_model=UserRead)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    statement = select(User).where(User.email == user.email)
    existing_user = db.exec(statement).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    new_user = User(name=user.name, email=user.email)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


@app.get("/users/{user_id}", response_model=UserRead)
def read_user(user_id: int, db: Session = Depends(get_db)):
    user = db.get(User, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@app.get("/companies/", response_model=list[CompanyRead])
def get_all_companies(db: Session = Depends(get_db)):
    companies = db.exec(select(Companies)).all()
    return companies


@app.get("/companies/{company_id}", response_model=CompanyRead)
def get_company(company_id: int, db: Session = Depends(get_db)):
    company = db.get(Companies, company_id)
    if not company:
        raise HTTPException(status_code=404, detail="Company not found")
    return company


@app.post("/companies/", response_model=CompanyRead)
def create_company(company: CompanyCreate, db: Session = Depends(get_db)):
    new_company = Companies(
        company_name=company.company_name,
        industry=company.industry,
        country=company.country
    )
    db.add(new_company)
    db.commit()
    db.refresh(new_company)
    return new_company


@app.post("/companies/random", response_model=list[CompanyRead])
def create_random_companies(db: Session = Depends(get_db), count: int = 100):
    new_companies = []

    for _ in range(count):
        company_data = CompanyCreate(
            company_name=fake.company(),
            industry=fake.bs(),
            country=fake.country()
        )
        new_company = Companies(
            company_name=company_data.company_name,
            industry=company_data.industry,
            country=company_data.country
        )
        db.add(new_company)
        new_companies.append(new_company)

    db.commit()
    for company in new_companies:
        db.refresh(company)

    return new_companies


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="localhost", port=8000, reload=True)
