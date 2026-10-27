import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.main import app
from app.db.base import Base

# Setup test database
SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def setup_db():
    Base.metadata.create_all(bind=engine)

def teardown_db():
    Base.metadata.drop_all(bind=engine)

client = TestClient(app)

def test_register_user():
    setup_db()
    response = client.post(
        "/api/v1/auth/register",
        json={"email": "test@example.com", "password": "password123"}
    )
    assert response.status_code == 201
    assert response.json()["email"] == "test@example.com"
    teardown_db()

def test_duplicate_email():
    setup_db()
    client.post("/api/v1/auth/register", json={"email": "test@example.com", "password": "password123"})
    response = client.post("/api/v1/auth/register", json={"email": "test@example.com", "password": "password123"})
    assert response.status_code == 400
    teardown_db()
