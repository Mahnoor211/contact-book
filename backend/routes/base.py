from fastapi import FastAPI, Depends
from db import Base, engine, get_db
from sqlalchemy.orm import Session
from models.users import User

Base.metadata.create_all(bind=engine)

app = FastAPI()


@app.get("/")
async def index():
    return {"message": "ok", "title": "contactbook"}


from pydantic import BaseModel, EmailStr


class UserRegisterSchemma(BaseModel):
    name: str
    email: EmailStr
    password: str


@app.post("/register")
def register_user(form_data: UserRegisterSchemma, db: Session = Depends(get_db)):
    user = User(name=form_data.name, email=form_data.email, password=form_data.password+"hashed")
    db.add(user)
    db.commit()
    db.refresh(user)
    return user
