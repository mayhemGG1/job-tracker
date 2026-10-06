import os
os.environ["DATABASE_URL"] = "sqlite:///:memory:"

import pytest
from app import app, db

@pytest.fixture
def client():
    app.config["TESTING"] = True
    with app.app_context():
        db.create_all()
        yield app.test_client()
        db.drop_all()
        db.session.remove()
