from sqlmodel import SQLModel, create_engine, Session

DATABASE_URL = "postgresql://postgres:Hamza@localhost:5432/postgres"

engine = create_engine(DATABASE_URL)


def create_db_and_tables():
    SQLModel.metadata.create_all(engine)


def get_db():
    with Session(engine) as session:
        yield session
