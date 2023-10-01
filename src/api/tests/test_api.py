import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from main import app, create_tables
from app.database_config import Base, DATABASE_URL as SQLALCHEMY_DATABASE_URL


engine = create_engine(SQLALCHEMY_DATABASE_URL)

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.create_all(bind=engine)


@pytest.fixture(scope="module")
def test_app():
    create_tables()
    client = TestClient(app)
    return client


@pytest.fixture(scope="module")
def test_db_session():
    return TestingSessionLocal()


def test_root(test_app):
    response = test_app.get("/")
    assert response.status_code == 200
    assert response.json() == {"Hello": "World"}


def test_login_for_access_token(test_app, test_db_session):

    # Make the login request
    response = test_app.post("/auth/login", data={"username": "admin", "password": "Webster301#"})

    # Perform assertions
    assert response.status_code == 200
    assert "access_token" in response.json()
    assert response.json()["token_type"] == "bearer"


@pytest.fixture(scope="module")
def test_token(test_app, test_db_session):
    # Make the login request
    response = test_app.post("/auth/login", data={"username": "admin", "password": "Webster301#"})
    
    # Perform assertions
    assert response.status_code == 200
    assert "access_token" in response.json()
    assert response.json()["token_type"] == "bearer"
    
    # Return the token for other tests
    return response.json()["access_token"]


def test_create_author(test_app, test_db_session, test_token):
    # Make the request, including the token in the headers
    response = test_app.post("/author/", 
                             json={"name": "Test Author"},
                             headers={"Authorization": f"Bearer {test_token}"})
    
    # Perform assertions
    assert response.status_code == 200
    assert "name" in response.json()
    assert response.json()["name"] == "Test Author"

    # Clean up - delete the created author
    author_id = response.json()["id"]
    test_app.delete(f"/author/{author_id}", headers={"Authorization": f"Bearer {test_token}"})


def test_create_book(test_app, test_db_session, test_token):
    # Make the request, including the token in the headers
    response = test_app.post("/book/",
                             json={"title": "Test Book", "author_id": 1, "pages": 10},
                             headers={"Authorization": f"Bearer {test_token}"})
    
    
    # Perform assertions
    assert response.status_code == 200
    assert "title" in response.json()
    assert response.json()["title"] == "Test Book"

    # Clean up - delete the created book
    book_id = response.json()["id"]
    test_app.delete(f"/book/{book_id}", headers={"Authorization": f"Bearer {test_token}"})

