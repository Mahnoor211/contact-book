import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from db import Base, get_db
from routes.base import app

TEST_DATABASE_URL = "sqlite:///./test_contact_book.db"

engine = create_engine(TEST_DATABASE_URL, connect_args={"check_same_thread": False})
TestSessionlocal = sessionmaker(bind=engine, autoflush=False, autocommit=False)


def test_get_db():
    try:
        db = TestSessionlocal()
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = test_get_db

Base.metadata.create_all(bind=engine)

client = TestClient(app)


@pytest.fixture(autouse=True)
def run_around_test():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    yield
    Base.metadata.drop_all(bind=engine)
    
def test_register_user_success():
    response = client.post("/register", json = {
        "name": "nobita",
        "email":"nobita543@gmail.com",
        "password":"gadgets"
    })
    
    assert response.status_code == 200
    data=response.json()
    assert data["name"]=="nobita"
    assert data["email"]=="nobita543@gmail.com"
    
def test_register_user_no_name():
    response = client.post("/register", json = {
        "email":"nobita543@gmail.com",
        "password":"gadgets"
    })
    
    assert response.status_code == 422
    
def test_register_user_no_email():
    response = client.post("/register", json = {
        "name": "nobita",
        "password":"gadgets"
    })
    
    assert response.status_code == 422
    
def test_register_user_no_password():
    response = client.post("/register", json = {
        "name": "nobita",
        "email":"nobita543@gmail.com",
    })
    
    assert response.status_code == 422
    
def test_register_user_no_data():
    response = client.post("/register")
    
    assert response.status_code == 422
    
def test_register_user_invalid_email():
    response = client.post("/register", json = {
        "name": "nobita",
        "email": "invalid email address",
        "password":"gadgets"
    })
    
    
def test_login_user_success():
    response = client.post("/login", json = {
        "email":"nobita543@gmail.com",
        "password":"gadgets"
    })
    
    assert response.status_code == 200
    
def test_login_user_no_email():
    response = client.post("/login", json = {
        "password":"gadgets"
    })
    
    assert response.status_code == 422
    
def test_login_user_no_password():
    response = client.post("/login", json = {
        "email": "nobita543@gmail.com"
    })
    
    assert response.status_code == 422
    
def test_login_user_no_data():
    response = client.post("/login",)
    
    assert response.status_code == 422