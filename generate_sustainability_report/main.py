from fastapi import FastAPI, Depends, HTTPException
from sqlmodel import Session, select
from models import User
from database import create_db_and_tables, get_db
from schemas import UserCreate, UserRead

app = FastAPI()

# Initialize the database and tables


def startup():
    create_db_and_tables()



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


if __name__ == "__main__":
    startup()
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)