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
    response = client.post(
        "/register",
        json={"name": "nobita", "email": "nobita543@gmail.com", "password": "gadgets"},
    )

    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "nobita"
    assert data["email"] == "nobita543@gmail.com"


def test_register_user_no_name():
    response = client.post(
        "/register", json={"email": "nobita543@gmail.com", "password": "gadgets"}
    )

    assert response.status_code == 422


def test_register_user_no_email():
    response = client.post("/register", json={"name": "nobita", "password": "gadgets"})

    assert response.status_code == 422


def test_register_user_no_password():
    response = client.post(
        "/register",
        json={
            "name": "nobita",
            "email": "nobita543@gmail.com",
        },
    )

    assert response.status_code == 422


def test_register_user_no_data():
    response = client.post("/register")

    assert response.status_code == 422


def test_register_user_invalid_email():
    response = client.post(
        "/register",
        json={
            "name": "nobita",
            "email": "invalid email address",
            "password": "gadgets",
        },
    )


def test_login_user_success():
    response = client.post(
        "/login", json={"email": "nobita543@gmail.com", "password": "gadgets"}
    )

    assert response.status_code == 200


def test_login_user_no_email():
    response = client.post("/login", json={"password": "gadgets"})

    assert response.status_code == 422


def test_login_user_no_password():
    response = client.post("/login", json={"email": "nobita543@gmail.com"})

    assert response.status_code == 422


def test_login_user_no_data():
    response = client.post(
        "/login",
    )

    assert response.status_code == 422

def test_register_contact_success():
    # First, register a user (because your DB is reset before each test)
    client.post(
        "/register",
        json={"name": "nobita", "email": "nobita543@gmail.com", "password": "gadgets"},
    )
    # Now, create a contact
    response = client.post(
        "/register-contact",
        json={
            "name": "Doraemon",
            "country_name": "Japan",
            "phone_number": "1234567890",
            "address": "Tokyo",
        },
    )

    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Doraemon"
    assert data["country_name"] == "Japan"
    assert data["phone_number"] == "1234567890"
    assert data["address"] == "Tokyo"


def test_register_contact_no_data():
    response = client.post("/register-contact")

    assert response.status_code == 422


def test_update_contact_success():
    # First create a contact
    client.post(
        "/register-contact",
        json={
            "name": "Doraemon",
            "country_name": "Japan",
            "phone_number": "1234567890",
            "address": "Tokyo",
        },
    )

    # Update the contact
    response = client.put(
        "/update-contact/1",
        json={
            "name": "Dorami",
            "country_name": "Japan",
            "phone_number": "9876543210",
            "address": "Kyoto",
        },
    )

    assert response.status_code == 200
    assert response.json()["message"] == "updated successsfulluy"


def test_update_contact_not_found():
    response = client.put(
        "/update-contact/999",
        json={
            "name": "Someone",
            "country_name": "Nowhere",
            "phone_number": "0000000000",
            "address": "Unknown",
        },
    )

    assert response.status_code == 200
    assert response.json()["message"] == "contact not found"


def test_partial_update_contact_success():
    client.post(
        "/register-contact",
        json={
            "name": "Doraemon",
            "country_name": "Japan",
            "phone_number": "1234567890",
            "address": "Tokyo",
        },
    )

    response = client.patch(
        "/update-contact/1",
        json={
            "phone_number": "111222333",
        },
    )

    assert response.status_code == 200
    assert response.json()["message"] == "updated successsfulluy"


def test_partial_update_contact_not_found():
    response = client.patch(
        "/update-contact/999",
        json={
            "phone_number": "111222333",
        },
    )

    assert response.status_code == 200
    assert response.json()["message"] == "contact not found"


def test_delete_contact_success():
    client.post(
        "/register-contact",
        json={
            "name": "Doraemon",
            "country_name": "Japan",
            "phone_number": "1234567890",
            "address": "Tokyo",
        },
    )

    response = client.delete("/delete-contact/1")

    assert response.status_code == 200
    assert response.json()["message"] == "deleted successsfulluy"


def test_delete_contact_not_found():
    response = client.delete("/delete-contact/999")

    assert response.status_code == 200
    assert response.json()["message"] == "contact not found"


def test_get_contact_success():
    client.post(
        "/register-contact",
        json={
            "name": "Doraemon",
            "country_name": "Japan",
            "phone_number": "1234567890",
            "address": "Tokyo",
        },
    )

    response = client.get("/get-contact/1")

    assert response.status_code == 200
    assert response.json()["message"] == "OK"
    assert response.json()["contact"]["name"] == "Doraemon"


def test_get_contact_not_found():
    response = client.get("/get-contact/999")

    assert response.status_code == 200
    assert response.json()["message"] == "contact not found"


def test_get_contacts_success():
    # Add two contacts
    client.post(
        "/register-contact",
        json={
            "name": "Doraemon",
            "country_name": "Japan",
            "phone_number": "1234567890",
            "address": "Tokyo",
        },
    )
    client.post(
        "/register-contact",
        json={
            "name": "Shizuka",
            "country_name": "Japan",
            "phone_number": "0987654321",
            "address": "Osaka",
        },
    )

    response = client.get("/get-contacts")

    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) == 2
