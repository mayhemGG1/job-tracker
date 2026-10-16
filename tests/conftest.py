import os
os.environ["DATABASE_URL"] = "sqlite:///:memory:"

import pytest
from app import app, db, User

@pytest.fixture
def client():
    app.config["TESTING"] = True
    with app.app_context():
        db.create_all()
        yield app.test_client()
        db.drop_all()
        db.session.remove()

@pytest.fixture
def user(client):
    u = User(email="test@example.com")
    u.set_password("password123")
    db.session.add(u)
    db.session.commit()
    return u

@pytest.fixture
def auth_client(client, user):
    client.post("/login", data={"email": "test@example.com", "password": "password123"})
    return client
